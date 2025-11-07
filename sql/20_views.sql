-- Vistas analíticas para el caso Finanzas

-- Vista 1: KPI de ejecución por área y partida
CREATE VIEW IF NOT EXISTS vw_kpi_ejecucion AS
SELECT
    g.area,
    g.partida,
    CAST(p.presupuesto AS DECIMAL(18,2)) as presupuesto,
    CAST(SUM(g.importe) AS DECIMAL(18,2)) as gasto_acumulado,
    CAST(p.presupuesto - SUM(g.importe) AS DECIMAL(18,2)) as presupuesto_restante,
    CAST(SUM(g.importe) / p.presupuesto AS DECIMAL(5,4)) as kpi_ejecucion,
    CAST(SUM(g.importe) * 100.0 / p.presupuesto AS DECIMAL(5,2)) as porcentaje_ejecucion
FROM clean_gastos g
JOIN clean_presupuesto p ON g.area = p.area AND g.partida = p.partida
GROUP BY g.area, g.partida, p.presupuesto;

-- Vista 2: Ejecución agregada por área
CREATE VIEW IF NOT EXISTS vw_ejecucion_area AS
SELECT
    area,
    CAST(SUM(presupuesto) AS DECIMAL(18,2)) as presupuesto_total,
    CAST(SUM(gasto_acumulado) AS DECIMAL(18,2)) as gasto_total,
    CAST(SUM(presupuesto_restante) AS DECIMAL(18,2)) as restante_total,
    CAST(SUM(gasto_acumulado) * 100.0 / SUM(presupuesto) AS DECIMAL(5,2)) as porcentaje_ejecucion
FROM vw_kpi_ejecucion
GROUP BY area
ORDER BY porcentaje_ejecucion DESC;

-- Vista 3: Gastos por día
CREATE VIEW IF NOT EXISTS vw_gastos_diarios AS
SELECT
    fecha,
    CAST(SUM(importe) AS DECIMAL(18,2)) as importe_total,
    COUNT(*) as num_transacciones
FROM clean_gastos
GROUP BY fecha
ORDER BY fecha;

-- Vista 4: Áreas en riesgo (>80% ejecución)
CREATE VIEW IF NOT EXISTS vw_areas_riesgo AS
SELECT *
FROM vw_kpi_ejecucion
WHERE porcentaje_ejecucion > 80
ORDER BY porcentaje_ejecucion DESC;

-- Vista 5: Tendencia mensual
CREATE VIEW IF NOT EXISTS vw_tendencia_mensual AS
SELECT
    strftime('%Y-%m', fecha) as anio_mes,
    area,
    CAST(SUM(importe) AS DECIMAL(18,2)) as gasto_mensual
FROM clean_gastos
GROUP BY strftime('%Y-%m', fecha), area
ORDER BY anio_mes, area;
