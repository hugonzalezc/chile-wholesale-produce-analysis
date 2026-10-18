-- Consultas de análisis sobre la tabla `precios` (ver sql/01_crear_tablas.sql).
-- Cada bloque "-- Qn" es una consulta. Se ejecutan todas con: python src/consultas.py

-- Q1 · Panorama del dataset (esperado: 1297334 filas, 82 productos, 12 mercados, 9 regiones)
SELECT COUNT(*)                 AS filas,
       COUNT(DISTINCT producto) AS productos,
       COUNT(DISTINCT mercado)  AS mercados,
       COUNT(DISTINCT region)   AS regiones,
       MIN(fecha)               AS desde,
       MAX(fecha)               AS hasta
FROM precios;

-- Q2 · Filas por año (esperado: las del README de datos crudos; 2025 con 201 filas menos)
SELECT anio, COUNT(*) AS filas
FROM precios
GROUP BY anio
ORDER BY anio;

-- Q3 · Filas por región (esperado: Región Metropolitana ≈ 38,9%)
SELECT region,
       COUNT(*) AS filas,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM precios), 1) AS pct_filas
FROM precios
GROUP BY region
ORDER BY filas DESC;

-- Q4 · Participación extranjera por año, de enero a septiembre (P3, medida por filas)
--      esperado: global 8,81 → 10,89; sin los seis productos casi siempre importados 2,95 → 4,72
SELECT anio,
       ROUND(100.0 * AVG(origen_tipo = 'Extranjero'), 2) AS pct_extranjero,
       ROUND(100.0 * AVG(CASE WHEN producto NOT IN ('Camote', 'Coco', 'Jengibre', 'Mango', 'Piña', 'Plátano')
                              THEN origen_tipo = 'Extranjero' END), 2) AS pct_sin_6_productos
FROM precios
WHERE mes <= 9
GROUP BY anio
ORDER BY anio;

-- Q5 · Tomate en bandeja de 18 kilos: precio promedio por año, ponderado por volumen y simple
--      (ponderado = SUM(precio × volumen) / SUM(volumen), como define ODEPA el precio promedio; CLP nominales)
SELECT anio,
       COUNT(*)                                            AS filas,
       ROUND(SUM(precio_prom * volumen) / SUM(volumen), 0) AS precio_ponderado,
       ROUND(AVG(precio_prom), 0)                          AS precio_simple
FROM precios
WHERE producto = 'Tomate' AND unidad = '$/bandeja 18 kilos'
GROUP BY anio
ORDER BY anio;