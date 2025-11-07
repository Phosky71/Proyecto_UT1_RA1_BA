# Ejecución Presupuestaria vs Gasto — Periodo 2025-01-01 a 2025-10-27

**Informe de Análisis Financiero**

---

## 📊 Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| **Presupuesto Total** | 3,137,290.00 € |
| **Gasto Acumulado** | 1,245,914.49 € |
| **Presupuesto Restante** | 1,891,375.51 € |
| **% Ejecución Global** | 39.71% |

---

## 📖 Definiciones de KPIs

### KPI Principal: Ejecución Presupuestaria

**kpi_ejecucion = gasto_acumulado / presupuesto**

- **Unidad**: Ratio decimal (0.0 - 1.0+)
- **Interpretación**: 
  - < 0.7: Ejecución baja
  - 0.7 - 0.9: Ejecución normal
  - > 0.9: Riesgo de sobreejecución
- **Redondeo**: 4 decimales

### Porcentaje de Ejecución

**porcentaje_ejecucion = kpi_ejecucion × 100**

- **Unidad**: Porcentaje (%)
- **Redondeo**: 2 decimales

### Notas Importantes

- **IVA**: Los importes están expresados **sin IVA** (base imponible)
- **Periodificación**: Los gastos se asignan al mes de la fecha de transacción
- **Moneda**: Todos los importes en **euros (€)** con precisión DECIMAL(18,2)
- **Deduplicación**: Política "último gana" por _ingest_ts para duplicados

---

## 📈 Ejecución por Área

| area        |   presupuesto |   gasto_acumulado |   presupuesto_restante |   porcentaje_ejecucion |
|:------------|--------------:|------------------:|-----------------------:|-----------------------:|
| IT          |        636408 |         247077.52 |              389330.48 |                  38.82 |
| Marketing   |        676327 |         191743.34 |              484583.66 |                  28.35 |
| Operaciones |        551544 |         257689.42 |              293854.58 |                  46.72 |
| RRHH        |        685860 |         326631.84 |              359228.16 |                  47.62 |
| Ventas      |        587151 |         222772.37 |              364378.63 |                  37.94 |

---

## 🔝 Top 10 Partidas por Ejecución

| area        | partida    |   presupuesto |   gasto_acumulado |   porcentaje_ejecucion |
|:------------|:-----------|--------------:|------------------:|-----------------------:|
| RRHH        | Hardware   |         60538 |          45848.70 |                  75.74 |
| IT          | Hardware   |         46839 |          33442.09 |                  71.40 |
| RRHH        | Software   |        133530 |          89300.75 |                  66.88 |
| IT          | Viajes     |         22135 |          14236.93 |                  64.32 |
| Ventas      | Viajes     |        124917 |          74169.29 |                  59.37 |
| Operaciones | Software   |         61461 |          36286.15 |                  59.04 |
| Operaciones | Material   |         20673 |          12054.60 |                  58.31 |
| Operaciones | Publicidad |         69921 |          39441.58 |                  56.41 |
| RRHH        | Formacion  |        117206 |          63291.64 |                  54.00 |
| Operaciones | Formacion  |        105473 |          55867.87 |                  52.97 |

---

## ⚠️ Áreas en Riesgo (>80% Ejecución)

*No hay áreas en riesgo actualmente*

---

## 📅 Tendencia Mensual

### Gasto por Área y Mes (€)

| anio_mes   |       IT |   Marketing |   Operaciones |     RRHH |   Ventas |
|:-----------|---------:|------------:|--------------:|---------:|---------:|
| 2025-01    | 16472.08 |    24085.98 |      41498.80 | 43841.41 | 11679.37 |
| 2025-02    | 25313.93 |     9588.24 |      32337.51 | 26477.29 | 31803.70 |
| 2025-03    | 20434.97 |    25874.85 |      31184.39 | 27620.31 | 17976.01 |
| 2025-04    | 18483.57 |     5921.33 |      29741.08 | 34020.16 | 15609.59 |
| 2025-05    | 24138.07 |     9712.99 |      33452.62 | 94624.17 | 40618.35 |
| 2025-06    | 23154.08 |    27100.29 |      14980.45 | 28320.63 | 14529.01 |
| 2025-07    | 19522.20 |    32829.47 |       8406.88 | 14286.68 | 47686.24 |
| 2025-08    | 23140.65 |    20740.48 |      27551.96 | 16895.63 | 21677.47 |
| 2025-09    | 43760.90 |    17317.07 |      15204.98 | 32991.59 | 18839.62 |
| 2025-10    | 32657.07 |    18572.64 |      23330.75 |  7553.97 |  2353.01 |

---

## 📋 Detalle Completo: Todas las Partidas

| area        | partida    |   presupuesto |   gasto_acumulado |   presupuesto_restante |   porcentaje_ejecucion |
|:------------|:-----------|--------------:|------------------:|-----------------------:|-----------------------:|
| IT          | Formacion  |        134265 |          42388.28 |               91876.72 |                  31.57 |
| IT          | Hardware   |         46839 |          33442.09 |               13396.91 |                  71.40 |
| IT          | Material   |         51527 |          22818.69 |               28708.31 |                  44.28 |
| IT          | Personal   |        133578 |          33568.27 |              100009.73 |                  25.13 |
| IT          | Publicidad |        136915 |          42257.38 |               94657.62 |                  30.86 |
| IT          | Software   |        111149 |          58365.88 |               52783.12 |                  52.51 |
| IT          | Viajes     |         22135 |          14236.93 |                7898.07 |                  64.32 |
| Marketing   | Formacion  |         95607 |          45768.11 |               49838.89 |                  47.87 |
| Marketing   | Hardware   |         85398 |          19641.89 |               65756.11 |                  23.00 |
| Marketing   | Material   |        114389 |          24333.11 |               90055.89 |                  21.27 |
| Marketing   | Personal   |        124956 |          20514.71 |              104441.29 |                  16.42 |
| Marketing   | Publicidad |        137922 |          43829.70 |               94092.30 |                  31.78 |
| Marketing   | Software   |         50521 |          14624.20 |               35896.80 |                  28.95 |
| Marketing   | Viajes     |         67534 |          23031.62 |               44502.38 |                  34.10 |
| Operaciones | Formacion  |        105473 |          55867.87 |               49605.13 |                  52.97 |
| Operaciones | Hardware   |        124094 |          48581.95 |               75512.05 |                  39.15 |
| Operaciones | Material   |         20673 |          12054.60 |                8618.40 |                  58.31 |
| Operaciones | Personal   |         43085 |          22179.32 |               20905.68 |                  51.48 |
| Operaciones | Publicidad |         69921 |          39441.58 |               30479.42 |                  56.41 |
| Operaciones | Software   |         61461 |          36286.15 |               25174.85 |                  59.04 |
| Operaciones | Viajes     |        126837 |          43277.95 |               83559.05 |                  34.12 |
| RRHH        | Formacion  |        117206 |          63291.64 |               53914.36 |                  54.00 |
| RRHH        | Hardware   |         60538 |          45848.70 |               14689.30 |                  75.74 |
| RRHH        | Material   |        133699 |          49161.69 |               84537.31 |                  36.77 |
| RRHH        | Personal   |         80811 |          33613.09 |               47197.91 |                  41.59 |
| RRHH        | Publicidad |        119063 |          37119.68 |               81943.32 |                  31.18 |
| RRHH        | Software   |        133530 |          89300.75 |               44229.25 |                  66.88 |
| RRHH        | Viajes     |         41013 |           8296.29 |               32716.71 |                  20.23 |
| Ventas      | Formacion  |         44192 |           5538.30 |               38653.70 |                  12.53 |
| Ventas      | Hardware   |        137247 |          55241.87 |               82005.13 |                  40.25 |
| Ventas      | Material   |         33205 |          10895.87 |               22309.13 |                  32.81 |
| Ventas      | Personal   |         95032 |          33197.29 |               61834.71 |                  34.93 |
| Ventas      | Publicidad |         75309 |           8732.87 |               66576.13 |                  11.60 |
| Ventas      | Software   |         77249 |          34996.88 |               42252.12 |                  45.30 |
| Ventas      | Viajes     |        124917 |          74169.29 |               50747.71 |                  59.37 |

---

## 🚨 Registros en Cuarentena

*Total filas rechazadas: 3*

| _quarantine_cause         |   cantidad |
|:--------------------------|-----------:|
| fecha_invalida            |          1 |
| importe_invalido          |          1 |
| partida_no_en_presupuesto |          1 |

---

## 📌 Contexto del Informe

- **Fuente de datos**: 
  - `project/data/drops/gastos.csv`
  - `project/data/drops/presupuesto.csv`
- **Periodo cubierto**: 2025-01-01 a 2025-10-27
- **Última actualización**: 2025-11-07 00:22:36 UTC
- **Almacenamiento por capas**:
  - **Bronze (raw)**: `project/data/storage/bronze/`
  - **Silver (clean)**: `project/data/storage/silver/`
  - **Gold (analytics)**: `project/data/storage/gold/`
  - **Quarantine**: `project/data/quarantine/`
  - **SQLite**: `project/output/ut1.db`
- **Filas procesadas**:
  - Bronze (raw): 306 gastos, 35 presupuesto
  - Silver (clean): 296 gastos, 35 presupuesto
  - Gold (analytics): 35 KPIs
  - Quarantine: 3 rechazados

---

## 💡 Conclusiones y Acciones Recomendadas

### Análisis General
- ℹ️ La ejecución global es del 39.71%, existe margen de gasto.


### Recomendaciones

1. **Revisión de partidas en riesgo**: Evaluar las áreas con >80% de ejecución para evitar sobrecostes
2. **Reasignación presupuestaria**: Considerar transferencias desde áreas con baja ejecución
3. **Control mensual**: Establecer revisiones mensuales de las partidas críticas
4. **Aprobaciones**: Implementar doble aprobación para gastos en partidas con >90% de ejecución
5. **Cuarentena**: Revisar y corregir los registros rechazados para completar el análisis

---

## 🔄 Trazabilidad del Pipeline

Este reporte ha sido generado automáticamente mediante el pipeline de datos ETL con arquitectura de capas:

### Flujo de Datos

1. **Ingestión (Bronze)**: 
   - Carga con idempotencia basada en batch_id
   - Añade metadatos: _ingest_ts, _source_file, _batch_id
   - Almacena datos RAW en `data/storage/bronze/`

2. **Limpieza (Silver)**: 
   - Validación de tipos, rangos y dominios
   - Normalización de áreas según catálogo
   - Deduplicación con política "último gana" por _ingest_ts
   - Almacena datos CLEAN en `data/storage/silver/`
   - Envía rechazados a `data/quarantine/` con causa

3. **Analíticas (Gold)**:
   - Cálculo de KPIs de ejecución presupuestaria
   - Agregaciones por área y partida
   - Almacena métricas en `data/storage/gold/`

4. **Persistencia**:
   - SQLite (`output/ut1.db`) con vistas analíticas
   - Vistas: vw_kpi_ejecucion, vw_ejecucion_area, vw_areas_riesgo, vw_tendencia_mensual

5. **Reporte**:
   - Generación de este documento Markdown desde Gold
   - Almacena en `project/output/reporte.md`

### Clave Natural

- **Gastos**: (fecha, area_normalizada, partida)
- **Presupuesto**: (area_normalizada, partida)

### Política de Conflictos

En caso de duplicados, se aplica **"último gana"** basado en _ingest_ts (timestamp de ingesta).

### Arquitectura de Capas


---

*Generado automáticamente el {ultima_actualizacion}*  
*Pipeline: project/ingest/run.py*  
*Arquitectura: Bronze → Silver → Gold*
