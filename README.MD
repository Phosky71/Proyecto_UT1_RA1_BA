# Pipeline ETL Finanzas: Presupuesto vs Gasto

Este repositorio implementa un pipeline **ETL** ligero para el análisis de ejecución presupuestaria frente a gastos reales en un contexto financiero, basado en la estructura del repositorio Proyecto_UT1_RA1_BA. El pipeline cubre ingesta de datos **CSV**, limpieza y modelado, almacenamiento en capas (bronze, silver, gold), cuarentena para inválidos y generación de un reporte en Markdown sin visualizaciones. Incluye un generador de datos de ejemplo para pruebas y validación.

## Requisitos

- Python 3.11 o superior.

## Librerías Principales

- `pandas` para manipulación de datos.
- `sqlite3` (incluido en Python) para base de datos.
- `pyarrow` opcional para Parquet (usado **CSV** en esta versión).

## Editor Recomendado

VS Code, Jupyter Notebook o similar.

## Datos de Entrada

Archivos `gastos.csv` (fecha, área, partida, importe) y `presupuesto.csv` (área, partida, presupuesto) en `data/drops/`.

## Opcional

Node.js 22+ y npm ≥10.9.2 para publicación en Quartz/Pages (no implementado aquí).

## Instalación y Configuración

Instala dependencias ejecutando: pip install pandas pyarrow


Clona el repositorio base Proyecto_UT1_RA1_BA si no lo tienes.

Coloca este código en la carpeta `ingest/` y el generador en la raíz.

Asegúrate de que las carpetas `data/drops/`, `data/storage/`, `data/quarantine/` y `output/` existan (se crean automáticamente al ejecutar).

No se requiere configuración adicional; las rutas son relativas.

## Estructura del Repositorio

La estructura sigue el modelo de capas de datos (bronze para raw, silver para clean, gold para analytics) con trazabilidad e idempotencia.

Proyecto_UT1_RA1_BA/
├── data/
│ ├── drops/ # Archivos de ingesta (CSVs de entrada)
│ │ ├── gastos.csv # Datos de gastos
│ │ └── presupuesto.csv # Datos de presupuesto
│ ├── storage/
│ │ ├── bronze/ # Datos raw con metadatos
│ │ │ ├── gastos_raw.csv
│ │ │ └── presupuesto_raw.csv
│ │ ├── silver/ # Datos limpios y validados
│ │ │ ├── gastos_clean.csv
│ │ │ └── presupuesto_clean.csv
│ │ └── gold/ # KPIs y agregados analíticos
│ │ ├── kpi_ejecucion.csv
│ │ └── ejecucion_por_area.csv
│ └── quarantine/ # Filas inválidas con causas
│ ├── gastos_invalidos.csv
│ └── presupuesto_invalidos.csv
├── sql/ # Scripts SQL (schema, upserts, vistas)
│ ├── 00_schema.sql
│ ├── 10_upserts.sql
│ └── 20_views.sql
├── output/ # Salidas finales
│ ├── ut1.db # SQLite con vistas
│ └── reporte.md # Reporte generado
├── ingest/
│ └── run.py # Pipeline principal (ETL + reporte)
├── get_data.py # Generador de datos de ejemplo
└── README.md # Este archivo


## Cómo Ejecutar

### Generar Datos de Ejemplo (Opcional)

Para pruebas, genera datos sintéticos con casos edge (duplicados, inválidos, áreas no normalizadas): python ingest/get_data.py


Esto crea ~**300** filas en `gastos.csv` (fechas desde **2025**-01-01, importes random ≤10% del presupuesto) y 35 filas en `presupuesto.csv` (una por área-partida, 20k-150k €). Incluye pruebas como importe negativo, fecha inválida y partida inexistente.

### Ejecutar el Pipeline ETL

Ejecuta el pipeline completo:

python ingest/run.py


- **Paso 1: Ingestión (Bronze)**: Lee CSVs de `data/drops/`, añade metadatos (_ingest_ts **UTC**, _source_file, _batch_id via **MD5** para idempotencia). Guarda raw en `data/storage/bronze/`.

- **Paso 2: Limpieza (Silver)**: Normaliza áreas (e.g., *rrhh* → *RRHH*), valida tipos (datetime para fecha, numeric para importes), rangos (importe ≥0), dominios (partidas vs. presupuesto). Deduplica con clave natural y *último gana* por _ingest_ts. Envía inválidos a `data/quarantine/` con causa (e.g., *fecha_invalida*). Guarda clean en `data/storage/silver/`.

- **Paso 3: Modelado (Gold)**: Calcula KPIs (kpi_ejecucion = gasto_acumulado / presupuesto por área-partida), agregados por área. Guarda en `data/storage/gold/`.

- **Paso 4: Almacenamiento**: Crea SQLite `output/ut1.db` con schema, upserts para clean y vistas analíticas (e.g., vw_kpi_ejecucion, vw_tendencia_mensual).

- **Paso 5: Reporte**: Genera `output/reporte.md` con resumen, KPIs definidos, tablas (ejecución por área, top 10, riesgo >80%, tendencia mensual), contexto y conclusiones automáticas.

El script imprime logs de progreso, filas procesadas y estructura de salida. Es idempotente: reprocesar no duplica gracias a batch_id y deduplicación. Tiempo estimado: <1 min para datos de ejemplo.

## Ver Resultados

Consulta SQLite:

sqlite3 output/ut1.db
SELECT * FROM vw_kpi_ejecucion;


Lee reporte: Abre `output/reporte.md` en Markdown viewer.

Para datos reales: Reemplaza CSVs en `data/drops/` y re-ejecuta.

## Decisiones Técnicas y Supuestos

### Ingestión y Trazabilidad (Reto 1)

Batch simple (no micro-batch, pero extensible con scheduling). Idempotencia via batch_id único por archivo (hash de nombre+tamaño+mtime). Metadatos en todas las filas para auditoría. Checkpoint implícito en batch_id.

Supuesto: Múltiples CSVs posibles en drops/; concatena si hay.

### Limpieza y Modelado (Reto 2)

Tipado y Validación: `pd.to_datetime` para fecha (coerce errores), `pd.to_numeric` para importes/presupuesto (**DECIMAL** implícito en float, pero **SQL** usa **DECIMAL**(18,2)). Rangos: importe/presupuesto ≥0. Nulos/quarantine si inválidos.

Dominios: Partidas validadas contra presupuesto; áreas normalizadas con mapa fijo (**RRHH**, IT, Marketing, Ventas, Operaciones).

Deduplicación: Clave natural: gastos (fecha + area_normalizada + partida), presupuesto (area_normalizada + partida). Política: *Último gana* por _ingest_ts (sort descending, drop_duplicates keep='last'). Documentado en reporte.

Supuesto: Datos en **UTF**-8, fechas %Y-%m-%d, importes en € sin **IVA**. No modelado extra (e.g., no unidades × precio).

### Almacenamiento (Reto Implícito)

Capas: Bronze (raw **CSV**), Silver (clean **CSV**), Gold (analytics **CSV**). SQLite para queries relacionales con vistas útiles (e.g., vw_areas_riesgo). Upserts en **SQL** evitan duplicados.

No Parquet (usa **CSV** para simplicidad; cambiar a to_parquet() para eficiencia). No particionado temporal (bono pendiente; agregar por mes en gold).

Supuesto: Almacenamiento local; escalable a cloud.

### KPIs y Reporte (Reto 3)

KPIs: kpi_ejecucion = gasto_acumulado / presupuesto (ratio 0-1+), porcentaje_ejecucion = kpi ×**100**, presupuesto_restante = presupuesto - gasto. Definiciones en reporte con interpretación (baja <70%, normal 70-90%, riesgo >90%).

Reporte.md: Titular con periodo, resumen ejecutivo (tabla métricas), definiciones KPIs/notas (**IVA** sin incluir, periodificación por fecha), tablas (por área, top 10, riesgo, tendencia mensual pivot), cuarentena, contexto (fuentes, actualización **UTC**), conclusiones/acciones (e.g., alertas automáticas si >90%).

Supuesto: Tendencia mensual por anio_mes; top N=10. Sin gráficas. Opcional: Publicar en Quartz (agregar script npm).




