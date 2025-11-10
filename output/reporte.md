# Ejecución Presupuestaria vs Gasto — Periodo 2025-01-01 a 2025-10-27

**Informe de Análisis Financiero**

---

## 📊 Resumen Ejecutivo

| Métrica                | Valor           |
|------------------------|-----------------|
| **Presupuesto Total**  | 3,289,631.00 € |
| **Gasto Acumulado**    | 1,419,985.62 € |
| **Presupuesto Restante** | 1,869,645.38 € |
| **% Ejecución Global** | 43.17%    |

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
| IT          |        555195 |         217431.75 |              337763.25 |                  39.16 |
| Marketing   |        643346 |         284045.64 |              359300.36 |                  44.15 |
| Operaciones |        710150 |         360667.60 |              349482.40 |                  50.79 |
| RRHH        |        634531 |         270107.13 |              364423.87 |                  42.57 |
| Ventas      |        746409 |         287733.50 |              458675.50 |                  38.55 |

---

## 🔝 Top 10 Partidas por Ejecución

| area        | partida    |   presupuesto |   gasto_acumulado |   porcentaje_ejecucion |
|:------------|:-----------|--------------:|------------------:|-----------------------:|
| Operaciones | Formacion  |        106376 |          88896.15 |                  83.57 |
| Operaciones | Software   |        112756 |          90339.67 |                  80.12 |
| IT          | Publicidad |         42969 |          33473.25 |                  77.90 |
| Marketing   | Software   |         97227 |          67828.60 |                  69.76 |
| RRHH        | Hardware   |         92876 |          59941.37 |                  64.54 |
| Operaciones | Viajes     |         98475 |          63446.55 |                  64.43 |
| RRHH        | Personal   |        132366 |          84386.85 |                  63.75 |
| RRHH        | Publicidad |        104403 |          58416.73 |                  55.95 |
| Marketing   | Viajes     |        128824 |          67038.88 |                  52.04 |
| Ventas      | Viajes     |         86156 |          43802.33 |                  50.84 |

---

## ⚠️ Áreas en Riesgo (>80% Ejecución)

| area        | partida   |   presupuesto |   gasto_acumulado |   presupuesto_restante |   porcentaje_ejecucion |
|:------------|:----------|--------------:|------------------:|-----------------------:|-----------------------:|
| Operaciones | Formacion |        106376 |          88896.15 |               17479.85 |                  83.57 |
| Operaciones | Software  |        112756 |          90339.67 |               22416.33 |                  80.12 |

---

## 📅 Tendencia Mensual

### Gasto por Área y Mes (€)

| anio_mes   |       IT |   Marketing |   Operaciones |     RRHH |   Ventas |
|:-----------|---------:|------------:|--------------:|---------:|---------:|
| 2025-01    | 46762.60 |    38804.45 |      45031.43 | 26809.16 | 25039.96 |
| 2025-02    | 16510.37 |    35357.98 |      27561.02 | 26218.36 | 19034.77 |
| 2025-03    |  5299.44 |    41348.66 |      35243.88 | 28592.40 | 38491.76 |
| 2025-04    | 21695.15 |    18774.78 |      45352.13 | 21716.61 | 18938.06 |
| 2025-05    | 24648.01 |    30698.42 |      25880.52 | 18414.55 | 17349.00 |
| 2025-06    | 25049.13 |    28171.32 |      40934.80 | 24999.54 | 36907.57 |
| 2025-07    |  3930.88 |    42752.18 |      32819.27 | 44560.41 | 34260.23 |
| 2025-08    | 44869.72 |     5905.32 |      29247.56 | 17962.08 | 54339.79 |
| 2025-09    | 24977.18 |    32155.67 |      11599.89 | 52941.36 |  7364.95 |
| 2025-10    |  3689.27 |    10076.86 |      66997.10 |  7892.66 | 36007.41 |

---

## 📋 Detalle Completo: Todas las Partidas

| area        | partida    |   presupuesto |   gasto_acumulado |   presupuesto_restante |   porcentaje_ejecucion |
|:------------|:-----------|--------------:|------------------:|-----------------------:|-----------------------:|
| IT          | Formacion  |         25895 |          12133.71 |               13761.29 |                  46.86 |
| IT          | Hardware   |        136098 |          28049.23 |              108048.77 |                  20.61 |
| IT          | Material   |        110286 |          42328.75 |               67957.25 |                  38.38 |
| IT          | Personal   |         85956 |          34424.61 |               51531.39 |                  40.05 |
| IT          | Publicidad |         42969 |          33473.25 |                9495.75 |                  77.90 |
| IT          | Software   |        133456 |          61574.97 |               71881.03 |                  46.14 |
| IT          | Viajes     |         20535 |           5447.23 |               15087.77 |                  26.53 |
| Marketing   | Formacion  |         96993 |          44507.65 |               52485.35 |                  45.89 |
| Marketing   | Hardware   |         57988 |          13502.56 |               44485.44 |                  23.29 |
| Marketing   | Material   |        130656 |          48071.98 |               82584.02 |                  36.79 |
| Marketing   | Personal   |         36613 |          12808.43 |               23804.57 |                  34.98 |
| Marketing   | Publicidad |         95045 |          30287.54 |               64757.46 |                  31.87 |
| Marketing   | Software   |         97227 |          67828.60 |               29398.40 |                  69.76 |
| Marketing   | Viajes     |        128824 |          67038.88 |               61785.12 |                  52.04 |
| Operaciones | Formacion  |        106376 |          88896.15 |               17479.85 |                  83.57 |
| Operaciones | Hardware   |        115029 |          48818.82 |               66210.18 |                  42.44 |
| Operaciones | Material   |        135834 |          38042.54 |               97791.46 |                  28.01 |
| Operaciones | Personal   |         91823 |          21794.51 |               70028.49 |                  23.74 |
| Operaciones | Publicidad |         49857 |           9329.36 |               40527.64 |                  18.71 |
| Operaciones | Software   |        112756 |          90339.67 |               22416.33 |                  80.12 |
| Operaciones | Viajes     |         98475 |          63446.55 |               35028.45 |                  64.43 |
| RRHH        | Formacion  |         78467 |          20698.88 |               57768.12 |                  26.38 |
| RRHH        | Hardware   |         92876 |          59941.37 |               32934.63 |                  64.54 |
| RRHH        | Material   |         82521 |          34576.86 |               47944.14 |                  41.90 |
| RRHH        | Personal   |        132366 |          84386.85 |               47979.15 |                  63.75 |
| RRHH        | Publicidad |        104403 |          58416.73 |               45986.27 |                  55.95 |
| RRHH        | Software   |         50506 |           8218.86 |               42287.14 |                  16.27 |
| RRHH        | Viajes     |         93392 |           3867.58 |               89524.42 |                   4.14 |
| Ventas      | Formacion  |         68294 |          18232.72 |               50061.28 |                  26.70 |
| Ventas      | Hardware   |        143956 |          54151.39 |               89804.61 |                  37.62 |
| Ventas      | Material   |        131101 |          66439.65 |               64661.35 |                  50.68 |
| Ventas      | Personal   |        103387 |          40300.96 |               63086.04 |                  38.98 |
| Ventas      | Publicidad |        115176 |          44842.19 |               70333.81 |                  38.93 |
| Ventas      | Software   |         98339 |          19964.26 |               78374.74 |                  20.30 |
| Ventas      | Viajes     |         86156 |          43802.33 |               42353.67 |                  50.84 |

---

[//]: # ()
[//]: # (## 📌 Contexto del Informe)

[//]: # ()
[//]: # (- **Periodo cubierto**: 2025-01-01 a 2025-10-27)

[//]: # (- **Última actualización**: 2025-11-10 16:30:39 UTC)

[//]: # ()
[//]: # (---)
