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