# Precios y volúmenes en los mercados mayoristas de frutas y hortalizas de Chile (2020–2026)

Análisis exploratorio de los registros de comercialización de frutas y hortalizas en mercados mayoristas de Chile, con datos de ODEPA. Se limpian y auditan los datos (incluyendo unidades de venta no comparables entre sí) y se describen patrones de precio, volumen, origen y mercado con Python, SQL y un dashboard en Power BI. Se describen asociaciones y diferencias observadas, no causalidad.

> 🚧 **Proyecto en construcción.** Última actualización: [09-10-2026]

## Estado

- [x] Estructura del repositorio y documentación de los datos
- [x] Carga y auditoría de datos
- [x] Limpieza
- [ ] Análisis de volúmenes, precios y temporal
- [ ] Base de datos y consultas SQL
- [ ] Dashboard
- [ ] Conclusiones e informe

## Preguntas de investigación

| # | Pregunta | Resultado esperado | Respuesta |
| --- | --- | --- | --- |
| P1 | Para un mismo producto y unidad, ¿qué mercados muestran mayor variabilidad de precios entre 2020 y 2025, y qué cambio acumulado tuvieron? | *(tu hipótesis)* | Pendiente |
| P2 | Dentro de cada producto y unidad, ¿qué proporción del volumen se registra en mercados de la Región Metropolitana, y cambió entre 2020 y 2026? | *(tu hipótesis)* | Pendiente |
| P3 | Dentro de cada producto, ¿cómo ha evolucionado la participación del origen extranjero en el volumen entre 2020 y 2026? | *(tu hipótesis)* | Pendiente |
| P4 | ¿Cuánto del cambio nominal de precios entre 2020 y 2025 corresponde a inflación general, y qué productos subieron o bajaron en términos reales? | *(tu hipótesis)* | Pendiente |
| P5 | Dentro de un mismo producto y unidad, ¿la calidad reportada se asocia con diferencias de precio, y de qué magnitud? | *(tu hipótesis)* | Pendiente |
| P6 | ¿Qué productos muestran un patrón estacional estable, con los mismos meses de precio alto y bajo en años distintos? | *(tu hipótesis)* | Pendiente |
| P7 *(opcional)* | Si se ajusta una tendencia simple con 2020–2024, ¿cuánto se acerca a lo observado en 2025, frente a repetir el valor del mismo mes del año anterior? | *(tu hipótesis)* | Pendiente |

Las preguntas pueden ajustarse tras la auditoría de datos. Cualquier cambio o descarte se documenta en [`docs/decisiones.md`](docs/decisiones.md).

## Datos

- **Fuente:** Oficina de Estudios y Políticas Agrarias (ODEPA), conjunto "Precios mayoristas de frutas y hortalizas".
- **Periodo:** enero de 2020 a octubre de 2026 (2026 incompleto).
- **Tamaño:** 1.297.535 filas en 7 archivos CSV.
- **Licencia:** Creative Commons Attribution (CC BY).
- **Detalle, diccionario y supuestos:** [`data/raw/README.md`](data/raw/README.md)

## Hallazgos principales

*(Se completa al terminar el análisis, organizado por pregunta.)*

## Dashboard

*(Capturas al terminar.)*

## Estructura del repositorio

```text
chile-wholesale-produce-analysis/
├── README.md
├── data/
│   ├── raw/           # CSV originales de ODEPA (no se modifican)
│   ├── interim/       # datos intermedios (generados, no versionados)
│   └── processed/     # dataset limpio y base SQLite (generados, no versionados)
├── docs/
│   └── decisiones.md  # bitácora de decisiones de limpieza y análisis
├── notebooks/         # 01 a 06, en orden de ejecución
├── src/               # funciones reutilizables
├── sql/               # creación de tablas y consultas
├── dashboard/         # archivo de Power BI y capturas
├── reports/           # informe, resumen ejecutivo y presentación
└── images/            # gráficos usados en este README
```

## Herramientas

Python, Pandas, Matplotlib, Seaborn, SQLite, Power BI, Jupyter, Git.

## Cómo reproducirlo

*(Se completa al final: instalación y orden de ejecución de los notebooks.)*

## Limitaciones

- La unidad de `Volumen` no está especificada por la fuente; se trabaja con una hipótesis que se pone a prueba en la auditoría.
- Los volúmenes no se suman entre productos ni entre unidades distintas.
- 2026 es un año incompleto; las comparaciones anuales usan los mismos meses.
- Los precios son nominales, salvo en los análisis ajustados por inflación.
- Solo se cubren los mercados que ODEPA monitorea, no todo el comercio del país.
- Los resultados describen asociaciones, no relaciones causales.

*(Se amplía al terminar el análisis.)*

## Fuente y atribución

Datos: ODEPA, [Portal de Datos Abiertos](https://datos.odepa.gob.cl/), licencia CC BY.

_Proyecto desarrollado con asistencia de Claude (Anthropic) para la escritura de código y la redacción. Las decisiones de diseño, la verificación de resultados y las conclusiones fueron revisadas por mí._