-- Schema para el caso Finanzas: Presupuesto vs Gasto

-- Tabla RAW: gastos (Bronze)
CREATE TABLE IF NOT EXISTS raw_gastos(
    fecha TEXT,
    area TEXT,
    partida TEXT,
    importe TEXT,
    _ingest_ts TEXT,
    _source_file TEXT,
    _batch_id TEXT,
    area_normalizada TEXT,
    _quarantine_cause TEXT
);

-- Tabla RAW: presupuesto (Bronze)
CREATE TABLE IF NOT EXISTS raw_presupuesto(
    area TEXT,
    partida TEXT,
    presupuesto TEXT,
    _ingest_ts TEXT,
    _source_file TEXT,
    _batch_id TEXT,
    area_normalizada TEXT
);

-- Tabla CLEAN: gastos (Silver)
CREATE TABLE IF NOT EXISTS clean_gastos(
    fecha TEXT,
    area TEXT,
    partida TEXT,
    importe REAL,
    _ingest_ts TEXT,
    PRIMARY KEY (fecha, area, partida)
);

-- Tabla CLEAN: presupuesto (Silver)
CREATE TABLE IF NOT EXISTS clean_presupuesto(
    area TEXT,
    partida TEXT,
    presupuesto REAL,
    _ingest_ts TEXT,
    PRIMARY KEY (area, partida)
);

-- Tabla de cuarentena
CREATE TABLE IF NOT EXISTS quarantine_gastos(
    _reason TEXT,
    _row TEXT,
    _ingest_ts TEXT,
    _source_file TEXT,
    _batch_id TEXT
);
