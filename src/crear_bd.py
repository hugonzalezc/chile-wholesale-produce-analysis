"""Crea data/processed/precios.db (SQLite) a partir del dataset limpio.

Uso (desde la raíz del proyecto):  python src/crear_bd.py
"""
import re
import sqlite3
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
PARQUET = RAIZ / "data" / "processed" / "precios_limpio.parquet"
DB = RAIZ / "data" / "processed" / "precios.db"
SQL = RAIZ / "sql" / "01_crear_tablas.sql"
TAM = 100_000


def main():
    if not PARQUET.exists():
        raise SystemExit(f"No existe {PARQUET}. Ejecuta antes notebooks/02_limpieza.ipynb")

    df = pd.read_parquet(PARQUET)
    cols_cat = list(df.select_dtypes("category").columns)

    tablas, indices = re.split(r"^-- INDICES\s*$", SQL.read_text(encoding="utf-8"), flags=re.M)

    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript(tablas)

    for i in range(0, len(df), TAM):
        parte = df.iloc[i:i + TAM].copy()
        for c in cols_cat:
            parte[c] = parte[c].astype(str)
        parte["fecha"] = parte["fecha"].dt.strftime("%Y-%m-%d")
        parte["es_rm"] = parte["es_rm"].astype(int)
        parte.to_sql("precios", con, if_exists="append", index=False)
        print(f"  {min(i + TAM, len(df)):,} / {len(df):,} filas cargadas")

    con.executescript(indices)   # falla si hay filas duplicadas en la clave (D-12)
    con.commit()

    n = con.execute("SELECT COUNT(*) FROM precios").fetchone()[0]
    con.close()
    assert n == len(df), f"se cargaron {n} filas y el dataset tiene {len(df)}"
    print(f"Base creada: {DB} | {n:,} filas | {DB.stat().st_size / 1024**2:.0f} MB")


if __name__ == "__main__":
    main()