from pathlib import Path
import pandas as pd

PATRON = "precio_mayorista_fruta-hortaliza_*.csv"

COLUMNAS_ESPERADAS = [
    "Fecha", "ID region", "Region", "Mercado", "Subsector", "Producto",
    "Variedad / Tipo", "Calidad", "Unidad de comercializacion", "Origen",
    "Volumen", "Precio minimo", "Precio maximo", "Precio promedio",
]


def listar_archivos(raw_dir):
    """Devuelve los CSV crudos ordenados por nombre (y por tanto por año)."""
    return sorted(Path(raw_dir).glob(PATRON))


def leer_crudo(ruta):
    """Lee un CSV sin interpretar nada: todo como texto, sin convertir vacíos a NaN.
    Se usa utf-8-sig para que un posible BOM no contamine el primer nombre de columna."""
    return pd.read_csv(ruta, dtype=str, keep_default_na=False, encoding="utf-8-sig")