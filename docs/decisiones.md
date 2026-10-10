# Bitácora de decisiones

Registro de decisiones de diseño, limpieza y análisis, con su justificación. Cada entrada indica qué se decidió, qué alternativas había y por qué se eligió esta. Las más recientes van abajo.

## Plantilla

### D-00 · Título de la decisión
- **Fecha:** AAAA-MM-DD
- **Contexto:** qué problema o duda había
- **Decisión:** qué se hizo
- **Alternativas:** qué otras opciones se consideraron
- **Justificación:** por qué esta
- **Impacto:** qué cambia en el análisis o en las conclusiones

---

## Decisiones

### D-01 · Alcance temporal: 2020–2026
- **Fecha:** 2026-10-02
- **Contexto:** el portal de ODEPA publica datos desde 1994.
- **Decisión:** trabajar solo con 2020 a 2026.
- **Alternativas:** usar toda la serie histórica.
- **Justificación:** reduce el riesgo de cambios de nombres, categorías, unidades y mercados a lo largo de décadas. Si la auditoría muestra que los años anteriores son comparables, se puede ampliar.
- **Impacto:** las conclusiones valen para este periodo, no para el histórico completo.

### D-02 · Datos crudos intactos
- **Fecha:** 2026-10-02
- **Contexto:** hay que decidir si renombrar o modificar los CSV descargados.
- **Decisión:** no renombrar ni editar los archivos originales. Toda limpieza ocurre en los notebooks.
- **Alternativas:** estandarizar los nombres de archivo.
- **Justificación:** conserva la trazabilidad respecto de la fuente y permite reproducir todo desde cero.
- **Impacto:** el código de carga debe adaptarse a los nombres originales.

### D-03 · Qué se versiona en Git
- **Fecha:** 2026-10-02
- **Contexto:** los CSV pesan unos 30 MiB cada uno (dato de ODEPA para 2026; el resto, estimado).
- **Decisión:** versionar los CSV crudos e ignorar `data/interim/` y `data/processed/`.
- **Alternativas:** ignorar también los crudos y dejar solo instrucciones de descarga.
- **Justificación:** la licencia CC BY permite redistribuir con atribución, y quien clone el repo puede reproducir sin descargar. Los archivos generados cambian seguido y engordarían el historial.
- **Impacto:** el dataset limpio y la base SQLite se regeneran ejecutando los notebooks.

### D-04 · Análisis temporal descriptivo, sin forecasting
- **Fecha:** 2026-10-03
- **Contexto:** idea inicial de predecir los precios de 2027.
- **Decisión:** usar análisis descriptivo (por mes, año y estacionalidad). La predicción queda como pregunta opcional (P7), evaluada contra una línea base ingenua con datos de 2025.
- **Alternativas:** extrapolar una tendencia hasta 2027.
- **Justificación:** hay pocos años, 2026 está incompleto, los precios son nominales y no se incluyen causas externas. Una extrapolación sin validación sería poco defendible.
- **Impacto:** el proyecto describe patrones; no promete predicciones.

### D-05 · Preguntas reformuladas
- **Fecha:** 2026-10-03
- **Contexto:** las preguntas iniciales pedían causas ("por qué") y variables externas ausentes del dataset.
- **Decisión:** reformular a "qué se asocia con", comparar siempre dentro de un mismo producto y unidad, y reducir las variables externas a la inflación (IPC).
- **Alternativas:** mantener las preguntas originales.
- **Justificación:** el dataset permite describir y comparar, no explicar causas.
- **Impacto:** las razones de los patrones se presentan como hipótesis, no como conclusiones.

### D-06 · Hipótesis de trabajo sobre `Volumen`
- **Fecha:** 2026-10-03
- **Contexto:** la fuente no especifica la unidad de `Volumen`.
- **Decisión:** suponer que está en la unidad de comercialización de la fila, y ponerlo a prueba en el notebook 01. Los volúmenes no se suman entre productos ni entre unidades distintas.
- **Alternativas:** suponer una medida común (por ejemplo, kilos).
- **Justificación:** es la lectura más natural, pero no está confirmada; se consulta a ODEPA.
- **Impacto:** si la hipótesis falla, cambian las preguntas P2 y P3.

### D-07 · Comparaciones entre años con los mismos meses
- **Fecha:** 2026-10-03
- **Contexto:** 2026 llega solo hasta el 2 de octubre.
- **Decisión:** al comparar años, usar el mismo periodo del año en todos.
- **Alternativas:** comparar el año completo y descontar 2026.
- **Justificación:** evita ver caídas de volumen que son solo meses faltantes.
- **Impacto:** las comparaciones anuales cubren enero a septiembre.

### D-08 · Precios nominales
- **Fecha:** 2026-10-03
- **Contexto:** los precios vienen en pesos de cada fecha.
- **Decisión:** trabajar en valores nominales, salvo en P4, donde se ajusta por IPC.
- **Alternativas:** deflactar todo el análisis.
- **Justificación:** mantiene simple el análisis general y deja la inflación como pregunta aparte.
- **Impacto:** fuera de P4, los cambios de precio incluyen inflación.

### D-09 · Tipos de datos
- **Fecha:** 2026-10-04
- **Contexto:** los CSV se leyeron como texto para auditarlos (1.247 MB en memoria).
- **Decisión:** `Fecha` a datetime, las cuatro columnas numéricas a números (coma decimal) y las textuales a categorías, incluido `ID region`.
- **Justificación:** baja la memoria a 69 MB y acelera las agrupaciones. `ID region` es un identificador, no una cantidad.
- **Impacto:** al agrupar categorías se usa `observed=True`.

### D-10 · Filas sin transacción (volumen 0 y precios 0)
- **Fecha:** 2026-10-04
- **Contexto:** 201 filas (0,02%) tienen volumen y los tres precios en 0, siempre juntos.
- **Decisión (provisoria):** tratarlas como "sin transacción" y excluirlas de los análisis de precio y volumen.
- **Justificación:** un precio de 0 pesos no es creíble, y son muy pocas.
- **Impacto:** se revisa su distribución en el notebook 01 antes de confirmar.

**(Actualización)** Las 201 filas con volumen y precios en 0 son todas de 2025, 114 en Vega Modelo de Temuco, y las cinco principales son fruta. Se confirma excluirlas de los análisis de precio y volumen.

### D-11 · Valores extremos se conservan
- **Fecha:** 2026-10-04
- **Contexto:** los precios llegan a 999.990 (kiwi en bins de 450 kg) y los volúmenes a 1.100.000 (choclo por unidad).
- **Decisión:** no eliminar valores por su magnitud. Se comparan siempre dentro del mismo producto y unidad.
- **Justificación:** las series son coherentes: la escala depende de la unidad, no de un error. El choclo de 1,1 millones se vigila como posible atípico.
- **Impacto:** nunca se resumen precios ni volúmenes entre unidades distintas.

### D-12 · Sin duplicados; clave única
- **Fecha:** 2026-10-04
- **Contexto:** no hay duplicados exactos ni filas con la misma clave y valores distintos.
- **Decisión:** no deduplicar. La clave (fecha, mercado, producto, variedad, calidad, unidad, origen) identifica cada fila.
- **Impacto:** se usa como clave única en SQLite.

### D-13 · Variabilidad medida con el precio promedio
- **Fecha:** 2026-10-04
- **Contexto:** mínimo y máximo coinciden en el 55,4% de las filas, y la proporción sube de 2021 a 2026.
- **Decisión:** no usar el rango diario como medida de variabilidad. P1 mide la variación del precio promedio entre periodos.
- **Impacto:** el rango y la variación relativa quedan solo como indicador complementario, con esta salvedad.

### D-14 · Interpretación de `Volumen`
- **Fecha:** 2026-10-04
- **Contexto:** 36.416 filas (2,8%) tienen la aclaración "(volumen en unidades)" en la unidad, p. ej. `$/kilo (volumen en unidades)`.
- **Decisión:** el volumen se interpreta como expresado en la unidad de venta salvo que la etiqueta diga otra cosa. Las filas con aclaración no se suman con las demás.
- **Justificación:** la aclaración explícita solo aparece en algunas etiquetas. Es una inferencia, no confirmada por ODEPA.
- **Impacto:** los volúmenes solo se suman dentro de una misma base de medida.

**(Actualización)** Se probó la hipótesis con cuatro productos (manzana, lechuga, palta, tomate). Solo la manzana en bins la respalda con claridad (volumen mediano 16 para un envase de 400 kg). En el resto la prueba no distingue entre volumen en la unidad de venta y volumen en una medida común. En etiquetas "$/kilo (en caja de X kilos)" se desconoce si el volumen son cajas o kilos. Sigue pendiente la respuesta de ODEPA.

**(Cierre)** La aclaración "(volumen en unidades)" aparece solo en 5 productos: zapallo, cebolla, sandía, rabanito y ajo. En el resto se asume que el volumen va en la unidad de venta. Pendiente de confirmar con ODEPA.

### D-15 · Origen nacional frente a extranjero
- **Fecha:** 2026-10-04
- **Decisión:** se clasifica como extranjero un origen de la lista de 13 países (incluida "Importada(o)"); todo lo demás es nacional.
- **Justificación:** la lista es pequeña y explícita. El resto de `Origen` mezcla regiones, provincias y comunas, y no se unifica.
- **Impacto:** se usa en P3. La parte de P2 sobre origen fuera de la RM queda diferida.

**(Actualización)** Seis productos son extranjeros en ≥95% de sus filas (camote, coco, jengibre, mango, piña, plátano) y se excluyen de P3 por no ofrecer alternativa nacional. P3 se enfoca en palta, poroto verde, sandía, zapallo, cebolla, limón y ajo. Se descartan por pocas filas o por ruido: maracuyá, pera asiática, poroto granado y melón. P3 se calculará por volumen (dentro de cada producto y etiqueta) y se contrastará con el cálculo por filas.

### D-16 · Calidad ordinal (provisoria)
- **Fecha:** 2026-10-04
- **Decisión:** para P5, agrupar en Primera/1a, Segunda/2a y Tercera/3a, y excluir calibres y estados de madurez.
- **Impacto:** se confirma tras ver cuántas filas y productos quedan con al menos dos calidades en la misma unidad.

### D-17 · Precio por kilo como medida comparable (provisoria)
- **Fecha:** 2026-10-04
- **Contexto:** el mismo producto aparece con muchos envases (nectarín tiene 33 unidades distintas). Comparar solo "mismo producto y misma etiqueta" fragmenta el
  análisis, y la etiqueta dominante cubre un 59,5% de las filas.
- **Decisión:** calcular precio por kilo cuando la etiqueta lo permita. Verificado con palta: kilo directo ≈ 3.000 y bandeja de 10 kg ≈ 2.800.
- **Alternativas:** comparar solo dentro de cada etiqueta.
- **Impacto:** quedan fuera de la conversión las unidades sin kilos (lechuga por unidad, docenas de atados) y las que traen rangos. Las diferencias por envase, variedad y calidad se controlan aparte.
- **Estado:** se confirma después de revisar las 191 etiquetas (celda 18).

**(Actualización)** Las 191 etiquetas se clasifican con `src/unidades.py` en: kilo, kilos_envase, unidades, kilo_vol_unidades, unidades_vol_unidades, rango y otro. `precio_kg` solo se calcula para kilo, kilos_envase y kilo_vol_unidades. Las demás se comparan dentro de su propia etiqueta.

**(Cierre)** `precio_kg` cubre el 69,9% de las filas. Quedan sin precio por kilo las unidades (28,4%), los rangos (0,9%) y dos etiquetas en gramos. La razón entre el mayor y el menor precio por kilo de un producto va de 2,4 a 3,7 en los seis productos más dispersos: no hay falla grosera, pero tampoco validación. La validación controlada (mismo mercado, fecha, variedad y calidad entre dos etiquetas) se hace en el análisis de precios.

### D-18 · Ponderación al agregar precios (provisoria)
- **Contexto:** la ponderación por volumen mezcla pesos de distinta base cuando se agrupan etiquetas.
- **Decisión:** dentro de una misma etiqueta, ponderar por volumen. Entre etiquetas, usar volumen × kilos por unidad, y comparar siempre contra la mediana sin ponderar.
- **Justificación:** el ponderado entre etiquetas depende de la hipótesis sobre `Volumen`, no confirmada. Si ambos métodos coinciden, la conclusión es más robusta.

### D-19 · Formato y unidad de análisis
- **Fecha:** 2026-10-04
- **Decisión:** el dataset limpio se guarda en Parquet, con nombres de columna en minúsculas y sin espacios. La unidad de análisis de precios es `precio_kg` cuando
  existe. Si no, el precio se compara dentro de una misma etiqueta de unidad.
- **Justificación:** Parquet conserva los tipos y se lee mucho más rápido que un CSV de 1,3 millones de filas. Los cambios de precio en el tiempo dentro de una misma etiqueta no requieren conversión alguna.
- **Impacto:** reemplaza el `precios_limpio.csv` previsto en la estructura inicial.

### D-20 · Método de P2
- **Fecha:** 2026-10-09
- **Decisión:** la participación de la RM se calcula dentro de cada (producto, unidad) y se resume con la mediana entre grupos. Panel de grupos que se usan en mercados de la RM y de fuera, presentes los 7 años y con al menos 500 filas. Solo enero a septiembre.
- **Justificación:** el volumen solo se suma dentro de una misma etiqueta (D-14). Sin la restricción, las etiquetas exclusivas de un mercado darían 0% o 100% por cómo se etiqueta, no por centralización. El panel evita que cambie la composición entre años.
- **Impacto:** el resultado vale para los mercados monitoreados por ODEPA (9 regiones). Se contrasta con filas y con kilos (celda 5).

### D-21 · Método de P3
- **Fecha:** 2026-10-09
- **Decisión:** la participación extranjera se mide por volumen, dentro de la etiqueta de unidad principal de cada producto con ambos orígenes (≥300 filas), para siete productos. Se contrasta con la proporción de filas.
- **Impacto:** no permite generalizar a productos casi siempre importados ni a los que casi no se importan.

### D-21 (reemplazada)
El método original (etiqueta principal por producto) se descartó: la etiqueta de unidad está ligada al origen (el limón importado se vende en `$/caja 24 kilos` y el nacional en otros envases), y en la palta dio 0% de importado cuando el conteo por filas daba 21–36%.
Nuevo método para P3: proporción de filas extranjeras por producto y año, contando todas las etiquetas. Contraste: proporción en kilos con las etiquetas `kilos_envase`, reportando la cobertura. Zapallo y sandía, solo por filas.

### D-22 · Cobertura cambiante entre años
- **Fecha:** 2026-10-09
- **Contexto:** hay grupos cuya participación en la RM cambia entre ~98% y ~2%, y el ajo con origen RM desaparece desde 2021.
- **Decisión:** investigar los mayores cambios de P2 (celda 13) antes de interpretarlos. Para ajo se compara desde 2021.
- **Impacto:** el resultado de P2 se reporta con la salvedad de que parte de la variabilidad es de cobertura y reporte.

### D-23 · Método de P2 revisado
- **Fecha:** 2026-10-09
- **Contexto:** los mayores cambios de participación de la RM por (producto, unidad) son etiquetas que aparecen o desaparecen: manzana `bandeja 18 kilos granel` (0% hasta 2022, luego 87–98% en Vega Central), lechuga `caja 24 unidades` (Lo Valledor pasa de ~170 filas por año a ~0 desde 2023), ají `caja 12 kilos` (cinco mercados hasta 2022, después casi solo Vega Central). El criterio de panel "presente los 7 años" aceptaba grupos con una o dos filas por año.
- **Decisión:** medida principal por producto en kilos (`kilos_envase`, cobertura ≥ 80% en kilos), que no depende de qué etiqueta use cada mercado. Contraste: grupos con presencia sostenida (≥20 filas por año, ≥5 en la RM y ≥5 fuera de ella) y proporción de filas.
- **Justificación:** sumar kilos entre etiquetas del mismo producto evita la rotación de etiquetas, a cambio de depender de la hipótesis de `Volumen` (D-14).
- **Impacto:** dos medidas con señales distintas (promedio por grupos −5 pp; 12 productos grandes en kilos +1 pp). Se reporta como "sin tendencia concluyente", con ambas cifras.

### D-24 · Medida en kilos de P3 limitada
- **Fecha:** 2026-10-09
- **Contexto:** `kilos_envase` excluye las etiquetas `$/kilo (en caja de N kilos)`. En la palta solo quedó `bandeja 10 kilos` (cobertura 0,29), la etiqueta importada, y el resultado (89–99%) fue un sesgo de selección.
- **Decisión:** la medida en kilos solo se reporta para ajo, cebolla, limón y poroto verde. Palta, zapallo y sandía quedan solo con la medida por filas.
- **Impacto:** la medida principal de P3 es filas con todas las etiquetas; la de kilos es un contraste parcial.

### D-25 · Cierre de P2
- **Fecha:** 2026-10-09
- **Contexto:** cuatro medidas de la participación de la RM dan señales distintas (promedio por grupo −5 a −8 pp; promedio por producto en kilos −7 pp; kilos totales +2 pp).
- **Decisión:** reportar las medidas con su rango (44% a 60%) y concluir "sin tendencia concluyente". La ponderación por volumen crudo entre etiquetas se descarta porque suma unidades distintas.
- **Justificación:** el resultado depende de si se pondera por producto o por kilos, y del conjunto de grupos elegido. Ninguna medida es "la verdadera".
- **Impacto:** el producto típico se descentraliza algo, pero el total de kilos no.

### D-26 · Cierre de P3
- **Fecha:** 2026-10-09
- **Decisión:** la medida de P3 es la proporción de filas extranjeras por producto y año. Los seis productos casi siempre importados explican el nivel global, no la tendencia.
- **Impacto:** la conclusión es por filas, no por volumen. La palta no permite separar un cambio real de un cambio de reporte.