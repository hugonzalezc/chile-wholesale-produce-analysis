# Datos crudos

**Fuente:** Oficina de Estudios y Políticas Agrarias (**ODEPA**)
**Enlaces:**
- Portal de ODEPA (fuente primaria): [Precios mayoristas de frutas y hortalizas](https://datos.odepa.gob.cl/dataset/precios-mayoristas-de-frutas-y-hortalizas)
- Portal nacional: [datos.gob.cl](https://datos.gob.cl/dataset/precios-mayoristas-de-frutas-y-hortalizas1)

**Licencia:** Creative Commons Attribution (CC BY). Fuente de los datos: ODEPA.
**Fecha de descarga:** 2026-10-02
**Periodo cubierto:** 2020–2026
**Patrón de nombre:** `precio_mayorista_fruta-hortaliza_AAAA.csv`

Los archivos no se modifican. Toda limpieza ocurre en `notebooks/02_limpieza.ipynb`.

## Archivos

| Archivo | Filas | Observaciones |
| --- | ---: | --- |
| precio_mayorista_fruta-hortaliza_2020.csv | 192.883 | |
| precio_mayorista_fruta-hortaliza_2021.csv | 194.776 | |
| precio_mayorista_fruta-hortaliza_2022.csv | 188.313 | |
| precio_mayorista_fruta-hortaliza_2023.csv | 188.192 | |
| precio_mayorista_fruta-hortaliza_2024.csv | 189.754 | |
| precio_mayorista_fruta-hortaliza_2025.csv | 202.029 | Más filas que 2024 en 9 de los 12 mercados; el mayor aumento es Lo Valledor (+3.932) |
| precio_mayorista_fruta-hortaliza_2026.csv | 141.588 | Año incompleto: datos hasta el 2 de octubre de 2026 |
| **Total** | **1.297.535** | |

## Diccionario de columnas

Las descripciones de la columna "Significado" provienen del diccionario de ODEPA cuando se indica "(según la fuente)"; el resto es inferido a partir de los datos.

| Columna | Significado | Tipo esperado | Pendiente de confirmar | Cómo se verifica |
| --- | --- | --- | --- | --- |
| Fecha | Fecha del precio comercializado (según la fuente) | datetime | ¿Es fecha de transacción o de reporte? | `to_datetime`, rango de fechas por archivo |
| ID region | Código de la región de Chile (según la fuente). Es un identificador, no una cantidad | texto/entero (entre comillas) | Sin pendientes | Revisar valores únicos |
| Region | Nombre de la región de Chile (según la fuente) | texto (categórica) | Sin pendientes | Cruce `ID region` × `Region` |
| Mercado | Mercado mayorista donde se comercializa el producto (según la fuente) | texto (categórica) | Resuelto: los 12 mercados aparecen en los 7 años | `value_counts()` por año |
| Subsector | Subsector del producto. La fuente indica "Frutas u Hortalizas" | texto (categórica) | Sin pendientes | `value_counts()` |
| Producto | Nombre del producto (según la fuente) | texto (categórica) | Sin pendientes | `value_counts()`, comparar listas por año |
| Variedad / Tipo | Variedad o tipo del producto (según la fuente) | texto (categórica) | Resuelto: el 36,1% de las filas dice “Sin especificar” | `value_counts(normalize=True)` |
| Calidad | Calidad del producto (según la fuente) | texto (categórica) | Resuelto: 70 valores que mezclan escalas (Primera, Segunda, Tercera), calibres y estados de madurez; no se asume que equivalgan entre productos | `value_counts()` por producto |
| Unidad de comercializacion | Unidad de comercialización del producto (según la fuente) | texto (categórica) | Resuelto: 191 etiquetas para 82 productos (hasta 33 por producto); se convierten a kilos cuando la etiqueta lo permite (D-17) | `value_counts()` por producto |
| Origen | Lugar de origen del producto (según la fuente) | texto (categórica) | Resuelto: 81 valores con niveles mezclados (región, provincia, comuna, país); 13 son países | `value_counts()` |
| Volumen | Volumen comercializado del producto (según la fuente) | numérico | Unidad de medida, que la fuente no especifica | Distribución por producto y unidad; comparación entre unidades |
| Precio minimo | Precio mínimo observado del producto en CLP (según la fuente) | numérico | ¿El precio es por la unidad de comercialización indicada? | Comparar entre mercados para el mismo producto y unidad |
| Precio maximo | Precio máximo observado del producto en CLP (según la fuente) | numérico | ¿El precio es por la unidad de comercialización indicada? | Idem |
| Precio promedio | Promedio ponderado por el volumen transado, en CLP (según la fuente) | numérico | Sin pendientes | Comparar las tres columnas fila a fila |

## Documentación disponible

ODEPA publica un diccionario de datos breve en su portal ([enlace](https://datos.odepa.gob.cl/dataset/precios-mayoristas-de-frutas-y-hortalizas/resource/580beca0-e87e-4dd4-9e8a-0bd92773f4a6)), con una frase por columna. No publica metodología ni la unidad de medida de `Volumen`. Dos definiciones relevantes, según la fuente:

- **Volumen:** "Volumen comercializado del producto" (sin unidad).
- **Precio promedio:** promedio según el volumen transado, en pesos chilenos (CLP).

Toda interpretación más allá de estas frases es inferida.

**Inconsistencia entre el diccionario y los datos** (confirmada al cargar los archivos):

- El diccionario declara `Precio minimo` y `Precio maximo` como enteros, pero los archivos los traen con coma decimal y cuatro decimales (por ejemplo, `1800,0000`).

## Notas de lectura

Confirmado al cargar los archivos (notebook 01):

- Separador de columnas: coma, con los textos entre comillas.
- Decimales con coma, por lo que conviene leer con `decimal=","`.
- Valores numéricos como `ID region` y `Volumen` vienen entre comillas.
- Los nombres de columnas tienen espacios, barras y mayúsculas; se estandarizan en la limpieza.

## Supuestos de trabajo

1. El volumen está expresado en la unidad de comercialización de cada fila, salvo en las etiquetas que dicen "(volumen en unidades)" (hipótesis no confirmada por ODEPA; ver D-14).
2. Los volúmenes no se suman entre productos. Dentro de un producto se suman entre etiquetas solo convirtiéndolos a kilos, y esa medida depende de la hipótesis anterior (D-23).
3. Para comparar precios entre etiquetas distintas se usa el precio por kilo cuando existe; dentro de una misma etiqueta, el precio promedio ponderado por volumen (D-17 y D-18).
4. Los precios están en pesos nominales (sin ajuste por inflación), salvo en el análisis de P4.

## Hallazgos de la auditoría (notebook 01)

- Los 7 encabezados son idénticos. Cada archivo contiene solo fechas de su año.
- No hay duplicados: la clave (fecha, mercado, producto, variedad, calidad, unidad, origen) es única.
- Cobertura: 9 regiones, 12 mercados (presentes los 7 años), 82 productos y 191 etiquetas de unidad.
- 201 filas (0,02%) con volumen y precios en 0, todas de 2025: se excluyen.
- Mínimo = máximo en el 55,4% de las filas (de 49,5% en 2021 a 61,8% en 2026).
- `Volumen`: 5 productos traen la aclaración "(volumen en unidades)" en la unidad (zapallo, cebolla, sandía, rabanito, ajo). En el resto se asume que va en la unidad de venta (inferencia, sin confirmar con ODEPA).
- `Origen` mezcla regiones, provincias, comunas y países. 13 valores son extranjeros.
- `Subsector` tiene dos valores (Frutas, Hortalizas y tubérculos), coherentes con el diccionario.
- `Variedad / Tipo` dice "Sin especificar" en el 36,1% de las filas.
- Las etiquetas de unidad rotan entre años: algunas aparecen o desaparecen según el mercado (D-23).