-- UPSERT para presupuesto
INSERT INTO clean_presupuesto (area, partida, presupuesto, _ingest_ts)
VALUES (:area, :part, :presup, :ts)
ON CONFLICT(area, partida) DO UPDATE SET
    presupuesto = excluded.presupuesto,
    _ingest_ts = excluded._ingest_ts;

-- UPSERT GASTOS
INSERT INTO clean_gastos (fecha, area, partida, importe, _ingest_ts)
VALUES (:fecha, :area, :part, :imp, :ts)
ON CONFLICT(fecha, area, partida)
DO UPDATE SET
    importe = excluded.importe,
    _ingest_ts = excluded._ingest_ts;
