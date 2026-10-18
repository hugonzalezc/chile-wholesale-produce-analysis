-- Tabla principal: una fila por (fecha, mercado, producto, variedad, calidad, unidad, origen)
CREATE TABLE precios (
    fecha        TEXT    NOT NULL,   -- AAAA-MM-DD
    id_region    TEXT    NOT NULL,
    region       TEXT    NOT NULL,
    mercado      TEXT    NOT NULL,
    subsector    TEXT    NOT NULL,
    producto     TEXT    NOT NULL,
    variedad     TEXT    NOT NULL,
    calidad      TEXT    NOT NULL,
    unidad       TEXT    NOT NULL,
    origen       TEXT    NOT NULL,
    volumen      INTEGER NOT NULL,   -- unidad no documentada por la fuente (ver D-14)
    precio_min   REAL    NOT NULL,
    precio_max   REAL    NOT NULL,
    precio_prom  REAL    NOT NULL,   -- CLP nominales
    anio         INTEGER NOT NULL,
    mes          INTEGER NOT NULL,
    origen_tipo  TEXT    NOT NULL,   -- 'Nacional' o 'Extranjero'
    tipo_unidad  TEXT    NOT NULL,
    kilos_unidad REAL,               -- NULL si la etiqueta no permite convertir a kilos
    precio_kg    REAL,               -- NULL si kilos_unidad es NULL
    es_rm        INTEGER NOT NULL    -- 1 si el mercado está en la Región Metropolitana
);

-- INDICES
-- Se crean después de cargar los datos, porque así la carga es mucho más rápida.
CREATE UNIQUE INDEX ux_clave ON precios (fecha, mercado, producto, variedad, calidad, unidad, origen);
CREATE INDEX ix_producto ON precios (producto);
CREATE INDEX ix_mercado  ON precios (mercado);
CREATE INDEX ix_anio_mes ON precios (anio, mes);
CREATE INDEX ix_region   ON precios (id_region);