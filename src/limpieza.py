import numpy as np
import pandas as pd

from .carga import listar_archivos, leer_crudo
from .unidades import parsear_unidad

COLS_NUM = ["Volumen", "Precio minimo", "Precio maximo", "Precio promedio"]

EXTRANJEROS = ["Ecuador", "Perú", "China", "Brasil", "EE.UU.", "México", "Bolivia",
               "Argentina", "Colombia", "Costa Rica", "Italia", "Paraguay", "Importada(o)"]

RENOMBRAR = {
    "Fecha": "fecha", "ID region": "id_region", "Region": "region",
    "Mercado": "mercado", "Subsector": "subsector", "Producto": "producto",
    "Variedad / Tipo": "variedad", "Calidad": "calidad",
    "Unidad de comercializacion": "unidad", "Origen": "origen",
    "Volumen": "volumen", "Precio minimo": "precio_min",
    "Precio maximo": "precio_max", "Precio promedio": "precio_prom",
}

COLS_CAT = ["id_region", "region", "mercado", "subsector", "producto", "variedad",
            "calidad", "unidad", "origen", "origen_tipo", "tipo_unidad"]


def cargar_tipado(raw_dir):
    """Lee los CSV, convierte fecha y números (coma decimal) y los une."""
    partes = []
    for ruta in listar_archivos(raw_dir):
        d = leer_crudo(ruta)
        d["Fecha"] = pd.to_datetime(d["Fecha"], format="%Y-%m-%d")
        for c in COLS_NUM:
            d[c] = pd.to_numeric(d[c].str.replace(",", ".", regex=False))
        partes.append(d)
    return pd.concat(partes, ignore_index=True)


def agregar_derivadas(df):
    """Agrega año, mes, tipo de origen, tipo de unidad y precio por kilo."""
    df = df.copy()
    df["anio"] = df["Fecha"].dt.year
    df["mes"] = df["Fecha"].dt.month
    df["origen_tipo"] = np.where(df["Origen"].isin(EXTRANJEROS), "Extranjero", "Nacional")

    info = {e: parsear_unidad(e) for e in df["Unidad de comercializacion"].unique()}
    df["tipo_unidad"] = df["Unidad de comercializacion"].map({e: v[0] for e, v in info.items()})
    df["kilos_unidad"] = (df["Unidad de comercializacion"]
                          .map({e: v[1] for e, v in info.items()}).astype(float))
    df["precio_kg"] = df["Precio promedio"] / df["kilos_unidad"]
    df["es_rm"] = df["ID region"].eq("13")
    return df


def limpiar(df):
    """Excluye las filas sin transacción (decisión D-10). Devuelve (df, registro)."""
    registro = [("filas iniciales", len(df))]
    sin_trans = df["Volumen"] == 0
    registro.append(("filas sin transacción excluidas", int(sin_trans.sum())))
    df = df[~sin_trans].copy()
    registro.append(("filas finales", len(df)))
    return df, pd.DataFrame(registro, columns=["paso", "filas"])


def finalizar(df):
    """Renombra columnas y convierte las textuales a categoría."""
    df = df.rename(columns=RENOMBRAR)
    for c in COLS_CAT:
        df[c] = df[c].astype("category")
    return df.reset_index(drop=True)


def validar(df):
    """Comprobaciones que deben cumplirse en el dataset limpio."""
    clave = ["fecha", "mercado", "producto", "variedad", "calidad", "unidad", "origen"]
    assert not df.duplicated(subset=clave).any(), "hay duplicados por clave"
    assert ((df["precio_min"] <= df["precio_prom"]) &
            (df["precio_prom"] <= df["precio_max"])).all(), "orden de precios roto"
    assert (df["volumen"] > 0).all(), "quedan volúmenes en cero"
    assert df[["fecha", "mercado", "producto", "unidad", "volumen", "precio_prom"]] \
        .notna().all().all(), "hay faltantes en columnas clave"
    return True