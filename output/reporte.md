# Ejecución Presupuestaria vs Gasto — Periodo 2025-01-03 a 2025-10-28

**Informe de Análisis Financiero**

---

## 📊 Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| **Presupuesto Total** | 2,886,762.00 € |
| **Gasto Acumulado** | 1,279,907.03 € |
| **Presupuesto Restante** | 1,606,854.97 € |
| **% Ejecución Global** | 44.34% |
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
| IT          |        551946 |         199476.65 |              352469.35 |                  36.14 |
| Marketing   |        710464 |         305226.26 |              405237.74 |                  42.96 |
| Operaciones |        465309 |         238019.24 |              227289.76 |                  51.15 |
| RRHH        |        458784 |         192511.16 |              266272.84 |                  41.96 |
| Ventas      |        700259 |         344673.72 |              355585.28 |                  49.22 |

---

## 🔝 Top 10 Partidas por Ejecución

| area        | partida   |   presupuesto |   gasto_acumulado |   porcentaje_ejecucion |
|:------------|:----------|--------------:|------------------:|-----------------------:|
| Ventas      | Personal  |        117280 |          91799.64 |                  78.27 |
| Operaciones | Material  |        138460 |         104126.73 |                  75.20 |
| Ventas      | Hardware  |         70063 |          47087.76 |                  67.21 |
| Operaciones | Personal  |         46439 |          28810.95 |                  62.04 |
| IT          | Material  |         33629 |          19001.60 |                  56.50 |
| Marketing   | Material  |         85533 |          47676.11 |                  55.74 |
| RRHH        | Material  |         58506 |          31553.23 |                  53.93 |
| Ventas      | Software  |        104834 |          55887.08 |                  53.31 |
| RRHH        | Formacion |         86777 |          45605.75 |                  52.56 |
| RRHH        | Hardware  |         81011 |          40858.27 |                  50.44 |

---

## ⚠️ Áreas en Riesgo (>80% Ejecución)

*No hay áreas en riesgo actualmente*

---

## 📅 Tendencia Mensual

### Gasto por Área y Mes (€)

| anio_mes   |       IT |   Marketing |   Operaciones |     RRHH |   Ventas |
|:-----------|---------:|------------:|--------------:|---------:|---------:|
| 2025-01    | 13291.34 |    26364.97 |      19138.93 | 10093.60 | 32464.66 |
| 2025-02    | 23331.83 |    23968.03 |      12476.40 | 25424.29 | 63249.59 |
| 2025-03    | 17056.07 |    31921.42 |      21321.28 | 22918.63 | 40808.73 |
| 2025-04    |  7416.59 |     9897.44 |      11677.34 | 33599.00 | 59204.70 |
| 2025-05    | 18530.01 |    42195.41 |      37432.32 | 32397.54 | 51420.72 |
| 2025-06    | 18735.55 |    19313.90 |      25355.73 |  1107.55 | 15168.49 |
| 2025-07    | 16900.72 |    58536.21 |      17190.48 |  8402.70 | 18275.51 |
| 2025-08    | 24472.97 |    30284.61 |      27657.35 | 26399.40 | 29720.32 |
| 2025-09    | 26599.19 |    26421.83 |      35092.25 | 14969.55 | 15485.43 |
| 2025-10    | 33142.38 |    36322.44 |      30677.16 | 17198.90 | 18875.57 |

---

## 📋 Detalle Completo: Todas las Partidas

| area        | partida    |   presupuesto |   gasto_acumulado |   presupuesto_restante |   porcentaje_ejecucion |
|:------------|:-----------|--------------:|------------------:|-----------------------:|-----------------------:|
| IT          | Formacion  |         91821 |          36910.74 |               54910.26 |                  40.20 |
| IT          | Hardware   |         57185 |          20347.84 |               36837.16 |                  35.58 |
| IT          | Material   |         33629 |          19001.60 |               14627.40 |                  56.50 |
| IT          | Personal   |        117643 |          26531.58 |               91111.42 |                  22.55 |
| IT          | Publicidad |        108836 |          49115.01 |               59720.99 |                  45.13 |
| IT          | Software   |         84700 |          25186.75 |               59513.25 |                  29.74 |
| IT          | Viajes     |         58132 |          22383.13 |               35748.87 |                  38.50 |
| Marketing   | Formacion  |         36522 |          15728.53 |               20793.47 |                  43.07 |
| Marketing   | Hardware   |        133384 |          51186.23 |               82197.77 |                  38.38 |
| Marketing   | Material   |         85533 |          47676.11 |               37856.89 |                  55.74 |
| Marketing   | Personal   |        132154 |          42986.45 |               89167.55 |                  32.53 |
| Marketing   | Publicidad |         89503 |          43246.40 |               46256.60 |                  48.32 |
| Marketing   | Software   |        129412 |          63309.70 |               66102.30 |                  48.92 |
| Marketing   | Viajes     |        103956 |          41092.84 |               62863.16 |                  39.53 |
| Operaciones | Formacion  |         30491 |           9749.11 |               20741.89 |                  31.97 |
| Operaciones | Hardware   |         26717 |           8548.96 |               18168.04 |                  32.00 |
| Operaciones | Material   |        138460 |         104126.73 |               34333.27 |                  75.20 |
| Operaciones | Personal   |         46439 |          28810.95 |               17628.05 |                  62.04 |
| Operaciones | Publicidad |         93322 |          44219.88 |               49102.12 |                  47.38 |
| Operaciones | Software   |        104275 |          33285.64 |               70989.36 |                  31.92 |
| Operaciones | Viajes     |         25605 |           9277.97 |               16327.03 |                  36.23 |
| RRHH        | Formacion  |         86777 |          45605.75 |               41171.25 |                  52.56 |
| RRHH        | Hardware   |         81011 |          40858.27 |               40152.73 |                  50.44 |
| RRHH        | Material   |         58506 |          31553.23 |               26952.77 |                  53.93 |
| RRHH        | Personal   |         23351 |           9938.05 |               13412.95 |                  42.56 |
| RRHH        | Publicidad |         42644 |           8017.60 |               34626.40 |                  18.80 |
| RRHH        | Software   |         56127 |          16225.89 |               39901.11 |                  28.91 |
| RRHH        | Viajes     |        110368 |          40312.37 |               70055.63 |                  36.53 |
| Ventas      | Formacion  |        105479 |          45317.50 |               60161.50 |                  42.96 |
| Ventas      | Hardware   |         70063 |          47087.76 |               22975.24 |                  67.21 |
| Ventas      | Material   |         78283 |          29491.19 |               48791.81 |                  37.67 |
| Ventas      | Personal   |        117280 |          91799.64 |               25480.36 |                  78.27 |
| Ventas      | Publicidad |        143848 |          49161.43 |               94686.57 |                  34.18 |
| Ventas      | Software   |        104834 |          55887.08 |               48946.92 |                  53.31 |
| Ventas      | Viajes     |         80472 |          25929.12 |               54542.88 |                  32.22 |

---

## 📌 Contexto del Informe

- **Periodo cubierto**: 2025-01-03 a 2025-10-28
- **Última actualización**: 2025-11-07 16:37:57 UTC

---