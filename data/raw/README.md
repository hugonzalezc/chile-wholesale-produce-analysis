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
| precio_mayorista_fruta-hortaliza_2025.csv | 202.029 | Más filas que el resto de los años; causa por determinar |
| precio_mayorista_fruta-hortaliza_2026.csv | 141.588 | Año incompleto: datos hasta el 2 de octubre de 2026 |
| **Total** | **1.297.535** | |

## Diccionario de columnas

Las descripciones de la columna "Significado" provienen del diccionario de ODEPA cuando se indica "(según la fuente)"; el resto es inferido a partir de los datos.

| Columna | Significado | Tipo esperado | Pendiente de confirmar | Cómo se verifica |
| --- | --- | --- | --- | --- |
| Fecha | Fecha del precio comercializado (según la fuente) | datetime | ¿Es fecha de transacción o de reporte? | `to_datetime`, rango de fechas por archivo |
| ID region | Código de la región de Chile (según la fuente). Es un identificador, no una cantidad | texto/entero (entre comillas) | Sin pendientes | Revisar valores únicos |
| Region | Nombre de la región de Chile (según la fuente) | texto (categórica) | ¿Coincide cada ID region con un único nombre de región? | Cruce `ID region` × `Region` |
| Mercado | Mercado mayorista donde se comercializa el producto (según la fuente) | texto (categórica) | ¿Cambia la lista de mercados con los años? | `value_counts()` por año |
| Subsector | Subsector del producto. La fuente indica "Frutas u Hortalizas" | texto (categórica) | Los datos muestran valores como "Hortalizas y tubérculos": ¿qué valores toma realmente y coinciden con los documentados? | `value_counts()` |
| Producto | Nombre del producto (según la fuente) | texto (categórica) | ¿Hay variantes de escritura del mismo producto entre años? | `value_counts()`, comparar listas por año |
| Variedad / Tipo | Variedad o tipo del producto (según la fuente) | texto (categórica) | ¿Qué proporción de filas dice "Sin especificar"? | `value_counts(normalize=True)` |
| Calidad | Calidad del producto (según la fuente) | texto (categórica) | Categorías existentes y si tienen el mismo significado para todos los productos | `value_counts()` por producto |
| Unidad de comercializacion | Unidad de comercialización del producto (según la fuente) | texto (categórica) | ¿Un mismo producto aparece con varias unidades? ¿Se pueden convertir entre sí? | `value_counts()` por producto |
| Origen | Lugar de origen del producto (según la fuente) | texto (categórica) | ¿Qué nivel geográfico usa (provincia, región, país) y es consistente? | `value_counts()` |
| Volumen | Volumen comercializado del producto (según la fuente) | numérico | Unidad de medida, que la fuente no especifica | Distribución por producto y unidad; comparación entre unidades |
| Precio minimo | Precio mínimo observado del producto en CLP (según la fuente) | numérico | ¿El precio es por la unidad de comercialización indicada? | Comparar entre mercados para el mismo producto y unidad |
| Precio maximo | Precio máximo observado del producto en CLP (según la fuente) | numérico | ¿El precio es por la unidad de comercialización indicada? | Idem |
| Precio promedio | Promedio ponderado por el volumen transado, en CLP (según la fuente) | numérico | ¿Se cumple mínimo ≤ promedio ≤ máximo en todas las filas? | Comparar las tres columnas fila a fila |

## Documentación disponible

ODEPA publica un diccionario de datos breve en su portal ([enlace](https://datos.odepa.gob.cl/dataset/precios-mayoristas-de-frutas-y-hortalizas/resource/580beca0-e87e-4dd4-9e8a-0bd92773f4a6)), con una frase por columna. No publica metodología ni la unidad de medida de `Volumen`. Dos definiciones relevantes, según la fuente:

- **Volumen:** "Volumen comercializado del producto" (sin unidad).
- **Precio promedio:** promedio según el volumen transado, en pesos chilenos (CLP).

Toda interpretación más allá de estas frases es inferida.

**Inconsistencias entre el diccionario y los datos** (observadas en las primeras filas; por confirmar en el notebook 01):

- El diccionario declara `Volumen`, `Precio minimo` y `Precio maximo` como enteros, pero los archivos traen los precios con coma decimal y cuatro decimales (por ejemplo, `1800,0000`).
- El diccionario describe `Subsector` como "Frutas u Hortalizas", pero los datos muestran, al menos, "Hortalizas y tubérculos".

## Notas de lectura

Observado en las primeras filas; por confirmar al cargar los archivos:

- Separador de columnas: coma, con los textos entre comillas.
- Decimales con coma, por lo que conviene leer con `decimal=","`.
- Valores numéricos como `ID region` y `Volumen` vienen entre comillas.
- Los nombres de columnas tienen espacios, barras y mayúsculas; se estandarizan en la limpieza.

## Supuestos de trabajo

1. El volumen está expresado en la unidad de comercialización de cada fila (hipótesis, no confirmada). Se pondrá a prueba en el notebook 01.
2. Los volúmenes no se suman entre productos ni entre unidades distintas.
3. El precio promedio es un promedio ponderado: al agregar por mes, mercado u origen se pondera por volumen, solo dentro del mismo producto y unidad.
4. Los precios están en pesos nominales (sin ajuste por inflación).

## Observaciones iniciales (provisorias)

- 2026 es un año incompleto (hasta el 2 de octubre). Las comparaciones anuales deben usar el mismo periodo en todos los años.
- En varias filas, precio mínimo, máximo y promedio coinciden. Falta medir cuántas.
- Un mismo producto (acelga) aparece con unidades de venta distintas según el mercado, y sus precios no son comparables entre sí.
- Estas observaciones se confirman o se descartan en la auditoría (`notebooks/01_carga_y_auditoria.ipynb`).

## Hallazgos de la auditoría (notebook 01)

- Los 7 encabezados son idénticos. Cada archivo contiene solo fechas de su año.
- No hay duplicados: la clave (fecha, mercado, producto, variedad, calidad, unidad, origen) es única.
- Cobertura: 9 regiones, 12 mercados (presentes los 7 años), 82 productos y 191 etiquetas de unidad.
- 201 filas (0,02%) con volumen y precios en 0, todas de 2025: se excluyen.
- Mínimo = máximo en el 55,4% de las filas (de 49,5% en 2021 a 61,8% en 2026).
- `Volumen`: 5 productos traen la aclaración "(volumen en unidades)" en la unidad (zapallo, cebolla, sandía, rabanito, ajo). En el resto se asume que va en la unidad de venta (inferencia, sin confirmar con ODEPA).
- `Origen` mezcla regiones, provincias, comunas y países. 13 valores son extranjeros.
- `Subsector` tiene dos valores (Frutas, Hortalizas y tubérculos), coherentes con el diccionario. Los precios traen 4 decimales con coma, aunque el diccionario los declara enteros.