import pandas as pd

# Valor de diciembre de 2023 en la serie referencial base 2023=100 (ver data/external/README.md)
R_DIC_2023 = 101.04


def empalmar(ruta_entrada, ruta_salida, r_dic_2023=R_DIC_2023):
    """Lleva los meses hasta dic 2023 (base 2018=100) al nivel de la base 2023=100,
    multiplicándolos por el factor de enlace FE = r_dic_2023 / índice(dic 2023, base 2018)."""
    raw = pd.read_csv(ruta_entrada)
    antes = raw["mes"] <= "2023-12"
    fe = r_dic_2023 / raw.loc[raw["mes"] == "2023-12", "ipc"].iloc[0]
    out = raw.copy()
    out.loc[antes, "ipc"] = (raw.loc[antes, "ipc"] * fe).round(2)
    out.to_csv(ruta_salida, index=False)
    return fe, out
