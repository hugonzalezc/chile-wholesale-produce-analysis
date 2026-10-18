"""Ejecuta sql/02_consultas_analisis.sql y muestra el resultado de cada consulta.

Uso (desde la raíz del proyecto):  python src/consultas.py
"""
import re
import sqlite3
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
DB = RAIZ / "data" / "processed" / "precios.db"
SQL = RAIZ / "sql" / "02_consultas_analisis.sql"


def main():
    if not DB.exists():
        raise SystemExit(f"No existe {DB}. Ejecuta antes: python src/crear_bd.py")

    texto = SQL.read_text(encoding="utf-8")
    bloques = [b for b in re.split(r"(?m)^(?=-- Q\d)", texto) if b.startswith("-- Q")]

    con = sqlite3.connect(DB)
    for b in bloques:
        titulo, _, consulta = b.partition("\n")
        notas = [l for l in consulta.splitlines() if l.startswith("--")]
        print("\n" + titulo)
        for n in notas:
            print(n)
        resultado = pd.read_sql_query(consulta, con)
        print(resultado.to_string(index=False))
    con.close()


if __name__ == "__main__":
    main()