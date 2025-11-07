"""
Pipeline finanzas: presupuesto vs gasto (ETL ligero)
Bronce → Plata → Oro → Quarantine → Reporte
Estructura real del proyecto
"""
import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# === Rutas según estructura real del repositorio ===
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "drops"
STORAGE = ROOT / "data" / "storage"
BRONZE = STORAGE / "bronze"
SILVER = STORAGE / "silver"
GOLD = STORAGE / "gold"
QUARANTINE = ROOT / "data" / "quarantine"
OUT = ROOT / "output"
SQL = ROOT / "sql"

# Crear carpetas necesarias
for folder in [BRONZE, SILVER, GOLD, QUARANTINE, OUT]:
    folder.mkdir(parents=True, exist_ok=True)

# ========== 1) INGESTA: BRONZE ==========
print("=" * 70)
print("RETO 1: INGESTIÓN - BRONZE (RAW)")
print("=" * 70)


def compute_batch_id(file_path):
    """Genera batch_id único basado en archivo para idempotencia"""
    stat = file_path.stat()
    content = f"{file_path.name}_{stat.st_size}_{stat.st_mtime}"
    return hashlib.md5(content.encode()).hexdigest()[:16]


files_gastos = sorted(DATA.glob("gastos.csv"))
files_presup = sorted(DATA.glob("presupuesto.csv"))
raw_gastos, raw_presup = [], []
utcnow = datetime.now(timezone.utc).isoformat()

for f in files_gastos:
    df = pd.read_csv(f, dtype=str)
    df["_source_file"] = f.name
    df["_ingest_ts"] = utcnow
    df["_batch_id"] = compute_batch_id(f)
    raw_gastos.append(df)
    print(f"✓ Ingesta: {f.name} → batch_id={df['_batch_id'].iloc[0]}")

for f in files_presup:
    df = pd.read_csv(f, dtype=str)
    df["_source_file"] = f.name
    df["_ingest_ts"] = utcnow
    df["_batch_id"] = compute_batch_id(f)
    raw_presup.append(df)
    print(f"✓ Ingesta: {f.name} → batch_id={df['_batch_id'].iloc[0]}")

gastos_raw = pd.concat(raw_gastos, ignore_index=True) if raw_gastos else pd.DataFrame()
presup_raw = pd.concat(raw_presup, ignore_index=True) if raw_presup else pd.DataFrame()

# Guardar en BRONZE
gastos_raw.to_csv(BRONZE / "gastos_raw.csv", index=False)
presup_raw.to_csv(BRONZE / "presupuesto_raw.csv", index=False)
print(f"\n✓ Bronze guardado: {BRONZE}")
print(f"  - gastos_raw.csv: {len(gastos_raw)} filas")
print(f"  - presupuesto_raw.csv: {len(presup_raw)} filas")

# ========== 2) LIMPIEZA: SILVER ==========
print("\n" + "=" * 70)
print("RETO 2: LIMPIEZA - SILVER (CLEAN)")
print("=" * 70)

AREAS_MAP = {
    "rrhh": "RRHH",
    "recursos humanos": "RRHH",
    "it": "IT",
    "informática": "IT",
    "informatica": "IT",
    "marketing": "Marketing",
    "ventas": "Ventas",
    "operaciones": "Operaciones"
}


def normalize_area(area):
    if pd.isna(area): return None
    clean = str(area).strip().lower()
    return AREAS_MAP.get(clean, str(area).strip().title())


# --- LIMPIEZA PRESUPUESTO ---
presup_df = presup_raw.copy()
presup_df["area_normalizada"] = presup_df["area"].apply(normalize_area)
presup_df["presupuesto"] = pd.to_numeric(presup_df["presupuesto"], errors="coerce")

presup_valid = (
        presup_df["area_normalizada"].notna() &
        presup_df["partida"].notna() &
        presup_df["presupuesto"].notna() &
        (presup_df["presupuesto"] >= 0)
)
presup_quar = presup_df.loc[~presup_valid].copy()
presup_clean = presup_df.loc[presup_valid].copy()

if not presup_clean.empty:
    presup_clean = presup_clean.sort_values("_ingest_ts", ascending=True)
    presup_clean = presup_clean.drop_duplicates(subset=["area_normalizada", "partida"], keep="last")

# --- LIMPIEZA GASTOS ---
gastos_df = gastos_raw.copy()
valid_partidas = set(presup_clean["partida"].unique()) if not presup_clean.empty else set()
gastos_df["area_normalizada"] = gastos_df["area"].apply(normalize_area)
gastos_df["fecha"] = pd.to_datetime(gastos_df["fecha"], errors="coerce")
gastos_df["importe"] = pd.to_numeric(gastos_df["importe"], errors="coerce")
gastos_df["_quarantine_cause"] = None
gastos_df.loc[gastos_df["fecha"].isna(), "_quarantine_cause"] = "fecha_invalida"
gastos_df.loc[gastos_df["importe"].isna() | (gastos_df["importe"] < 0), "_quarantine_cause"] = "importe_invalido"
if valid_partidas:
    gastos_df.loc[~gastos_df["partida"].isin(valid_partidas), "_quarantine_cause"] = "partida_no_en_presupuesto"

gastos_quar = gastos_df[gastos_df["_quarantine_cause"].notna()].copy()
gastos_clean = gastos_df[gastos_df["_quarantine_cause"].isna()].copy()

if not gastos_clean.empty:
    gastos_clean = gastos_clean.sort_values("_ingest_ts", ascending=True)
    gastos_clean = gastos_clean.drop_duplicates(subset=["fecha", "area_normalizada", "partida"], keep="last")

print(f"Presupuesto: {len(presup_df)} → Clean={len(presup_clean)}, Quarantine={len(presup_quar)}")
print(f"Gastos: {len(gastos_df)} → Clean={len(gastos_clean)}, Quarantine={len(gastos_quar)}")

# Guardar en SILVER
presup_clean.to_csv(SILVER / "presupuesto_clean.csv", index=False)
gastos_clean.to_csv(SILVER / "gastos_clean.csv", index=False)
print(f"\n✓ Silver guardado: {SILVER}")
print(f"  - presupuesto_clean.csv: {len(presup_clean)} filas")
print(f"  - gastos_clean.csv: {len(gastos_clean)} filas")

# Guardar en QUARANTINE
if not presup_quar.empty:
    presup_quar.to_csv(QUARANTINE / "presupuesto_invalidos.csv", index=False)
if not gastos_quar.empty:
    gastos_quar.to_csv(QUARANTINE / "gastos_invalidos.csv", index=False)
    print(f"\n✓ Quarantine guardado: {QUARANTINE}")
    print(f"  - gastos_invalidos.csv: {len(gastos_quar)} filas")
    print(f"  Causas: {gastos_quar['_quarantine_cause'].value_counts().to_dict()}")

# ========== 3) ORO: GOLD + ANALYTICS ==========
print("\n" + "=" * 70)
print("RETO 3: ORO - GOLD (ANALYTICS)")
print("=" * 70)

# Calcular KPIs para capa Gold
if not gastos_clean.empty and not presup_clean.empty:
    kpi_df = gastos_clean.groupby(["area_normalizada", "partida"], as_index=False)["importe"].sum()
    kpi_df.columns = ["area", "partida", "gasto_acumulado"]
    kpi_df = kpi_df.merge(
        presup_clean[["area_normalizada", "partida", "presupuesto"]],
        left_on=["area", "partida"],
        right_on=["area_normalizada", "partida"],
        how="left"
    )
    kpi_df["kpi_ejecucion"] = (kpi_df["gasto_acumulado"] / kpi_df["presupuesto"]).round(4)
    kpi_df["porcentaje_ejecucion"] = (kpi_df["kpi_ejecucion"] * 100).round(2)
    kpi_df["presupuesto_restante"] = (kpi_df["presupuesto"] - kpi_df["gasto_acumulado"]).round(2)

    # Guardar en GOLD (capa analítica)
    kpi_df.to_csv(GOLD / "kpi_ejecucion.csv", index=False)

    # Agregados por área
    area_agg = kpi_df.groupby("area", as_index=False).agg({
        "presupuesto": "sum",
        "gasto_acumulado": "sum",
        "presupuesto_restante": "sum"
    })
    area_agg["porcentaje_ejecucion"] = (area_agg["gasto_acumulado"] / area_agg["presupuesto"] * 100).round(2)
    area_agg.to_csv(GOLD / "ejecucion_por_area.csv", index=False)

    print(f"\n✓ Gold guardado: {GOLD}")
    print(f"  - kpi_ejecucion.csv: {len(kpi_df)} filas")
    print(f"  - ejecucion_por_area.csv: {len(area_agg)} filas")
else:
    kpi_df = pd.DataFrame()
    area_agg = pd.DataFrame()

# ========== 4) ALMACENAMIENTO: SQLITE ==========
print("\n" + "=" * 70)
print("ALMACENAMIENTO: SQLITE + VISTAS")
print("=" * 70)

DB = OUT / "ut1.db"
con = sqlite3.connect(DB)
con.executescript((SQL / "00_schema.sql").read_text(encoding="utf-8"))
print("✓ SQLite schema creado")

# Insertar raw
if not gastos_df.empty:
    gastos_df[[col for col in gastos_df.columns if not col.startswith("_quarantine")]].to_sql(
        "raw_gastos", con, if_exists="replace", index=False
    )
if not presup_df.empty:
    presup_df.to_sql("raw_presupuesto", con, if_exists="replace", index=False)

# Ejecutar upserts para clean
upsert_sql = (SQL / "10_upserts.sql").read_text(encoding="utf-8")
parts = upsert_sql.split("-- UPSERT GASTOS")
upsert_pres_stmt = parts[0].strip()
upsert_gastos_stmt = parts[1].strip()

for _, r in presup_clean.iterrows():
    con.execute(upsert_pres_stmt, {
        "area": r["area_normalizada"], "part": r["partida"], "presup": float(r["presupuesto"]), "ts": r["_ingest_ts"]
    })
for _, r in gastos_clean.iterrows():
    fecha_str = r["fecha"].strftime("%Y-%m-%d") if pd.notna(r["fecha"]) else None
    con.execute(upsert_gastos_stmt, {
        "fecha": fecha_str, "area": r["area_normalizada"], "part": r["partida"], "imp": float(r["importe"]),
        "ts": r["_ingest_ts"]
    })
con.commit()
print("✓ SQLite upserts completados")

# Crear vistas
con.executescript((SQL / "20_views.sql").read_text(encoding="utf-8"))
con.close()
print(f"✓ Base de datos: {DB}")

# ========== 5) REPORTE MARKDOWN ==========
print("\n" + "=" * 70)
print("RETO 4: REPORTE MARKDOWN")
print("=" * 70)

# Leer desde GOLD para el reporte
if (GOLD / "kpi_ejecucion.csv").exists():
    kpi_rep = pd.read_csv(GOLD / "kpi_ejecucion.csv")
    area_rep = pd.read_csv(GOLD / "ejecucion_por_area.csv")
else:
    kpi_rep = kpi_df
    area_rep = area_agg

# Calcular métricas para reporte
if not kpi_rep.empty:
    total_presup = kpi_rep["presupuesto"].sum()
    total_gasto = kpi_rep["gasto_acumulado"].sum()
    total_restante = total_presup - total_gasto
    ejecucion_global = (total_gasto / total_presup * 100) if total_presup > 0 else 0

    top_partidas = kpi_rep.sort_values("porcentaje_ejecucion", ascending=False).head(10)
    riesgo = kpi_rep[kpi_rep["porcentaje_ejecucion"] > 80].sort_values("porcentaje_ejecucion", ascending=False)

    # Tendencia mensual
    gastos_temp = pd.read_csv(SILVER / "gastos_clean.csv")
    gastos_temp["fecha"] = pd.to_datetime(gastos_temp["fecha"])
    gastos_temp["anio_mes"] = gastos_temp["fecha"].dt.to_period("M").astype(str)
    mensual = gastos_temp.groupby(["anio_mes", "area_normalizada"], as_index=False)["importe"].sum()
    mensual_pivot = mensual.pivot_table(index="anio_mes", columns="area_normalizada", values="importe", fill_value=0)

    periodo_ini = gastos_temp["fecha"].min()
    periodo_fin = gastos_temp["fecha"].max()
    periodo = f"{periodo_ini.date()} a {periodo_fin.date()}"
else:
    total_presup = total_gasto = total_restante = ejecucion_global = 0
    top_partidas = riesgo = mensual_pivot = kpi_rep = area_rep = pd.DataFrame()
    periodo = "N/A"

ultima_actualizacion = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

# Construir reporte completo (sin indentación para que Markdown funcione)
reporte = f"""# Ejecución Presupuestaria vs Gasto — Periodo {periodo}

**Informe de Análisis Financiero**

---

## 📊 Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| **Presupuesto Total** | {total_presup:,.2f} € |
| **Gasto Acumulado** | {total_gasto:,.2f} € |
| **Presupuesto Restante** | {total_restante:,.2f} € |
| **% Ejecución Global** | {ejecucion_global:.2f}% |

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

{area_rep.to_markdown(index=False, floatfmt=".2f") if not area_rep.empty else "*No hay datos disponibles*"}

---

## 🔝 Top 10 Partidas por Ejecución

{top_partidas[["area", "partida", "presupuesto", "gasto_acumulado", "porcentaje_ejecucion"]].to_markdown(index=False, floatfmt=".2f") if not top_partidas.empty else "*No hay datos disponibles*"}

---

## ⚠️ Áreas en Riesgo (>80% Ejecución)

{riesgo[["area", "partida", "presupuesto", "gasto_acumulado", "presupuesto_restante", "porcentaje_ejecucion"]].to_markdown(index=False, floatfmt=".2f") if not riesgo.empty else "*No hay áreas en riesgo actualmente*"}

---

## 📅 Tendencia Mensual

### Gasto por Área y Mes (€)

{mensual_pivot.to_markdown(floatfmt=".2f") if not mensual_pivot.empty else "*No hay datos de tendencia mensual*"}

---

## 📋 Detalle Completo: Todas las Partidas

{kpi_rep[["area", "partida", "presupuesto", "gasto_acumulado", "presupuesto_restante", "porcentaje_ejecucion"]].to_markdown(index=False, floatfmt=".2f") if not kpi_rep.empty else "*No hay datos disponibles*"}

---

## 🚨 Registros en Cuarentena

{"*Total filas rechazadas: " + str(len(gastos_quar)) + "*" if not gastos_quar.empty else "*No hay registros en cuarentena*"}

{gastos_quar.groupby("_quarantine_cause").size().reset_index(name="cantidad").to_markdown(index=False) if not gastos_quar.empty else ""}

---

## 📌 Contexto del Informe

- **Fuente de datos**: 
  - `project/data/drops/gastos.csv`
  - `project/data/drops/presupuesto.csv`
- **Periodo cubierto**: {periodo}
- **Última actualización**: {ultima_actualizacion}
- **Almacenamiento por capas**:
  - **Bronze (raw)**: `project/data/storage/bronze/`
  - **Silver (clean)**: `project/data/storage/silver/`
  - **Gold (analytics)**: `project/data/storage/gold/`
  - **Quarantine**: `project/data/quarantine/`
  - **SQLite**: `project/output/ut1.db`
- **Filas procesadas**:
  - Bronze (raw): {len(gastos_raw)} gastos, {len(presup_raw)} presupuesto
  - Silver (clean): {len(gastos_clean)} gastos, {len(presup_clean)} presupuesto
  - Gold (analytics): {len(kpi_rep)} KPIs
  - Quarantine: {len(gastos_quar)} rechazados

---

## 💡 Conclusiones y Acciones Recomendadas

### Análisis General
"""

# Análisis automático
if ejecucion_global > 90:
    reporte += f"- ⚠️ **ALERTA**: La ejecución global es del {ejecucion_global:.2f}%, existe riesgo de sobreejecución presupuestaria.\n"
elif ejecucion_global > 70:
    reporte += f"- ✓ La ejecución global es del {ejecucion_global:.2f}%, dentro de rangos normales.\n"
else:
    reporte += f"- ℹ️ La ejecución global es del {ejecucion_global:.2f}%, existe margen de gasto.\n"

if not riesgo.empty:
    reporte += "\n### Áreas que Requieren Atención\n\n"
    for _, row in riesgo.head(5).iterrows():
        reporte += f"- **{row['area']} - {row['partida']}**: {row['porcentaje_ejecucion']:.2f}% ejecutado. Restante: {row['presupuesto_restante']:.2f} €\n"

reporte += """

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
"""

# Guardar reporte
REPORTE_FILE = OUT / "reporte.md"
REPORTE_FILE.write_text(reporte, encoding="utf-8")
print(f"\n✓ Reporte generado: {REPORTE_FILE}")
print(f"  {len(reporte)} caracteres")

print("\n" + "=" * 70)
print("✓✓✓ PIPELINE COMPLETADO EXITOSAMENTE ✓✓✓")
print("=" * 70)
print(f"""
📁 Estructura de salida:

   Bronze (RAW):
   └─ {BRONZE}/
      ├─ gastos_raw.csv ({len(gastos_raw)} filas)
      └─ presupuesto_raw.csv ({len(presup_raw)} filas)

   Silver (CLEAN):
   └─ {SILVER}/
      ├─ gastos_clean.csv ({len(gastos_clean)} filas)
      └─ presupuesto_clean.csv ({len(presup_clean)} filas)

   Gold (ANALYTICS):
   └─ {GOLD}/
      ├─ kpi_ejecucion.csv ({len(kpi_rep) if not kpi_rep.empty else 0} filas)
      └─ ejecucion_por_area.csv ({len(area_rep) if not area_rep.empty else 0} filas)

   Quarantine:
   └─ {QUARANTINE}/
      └─ gastos_invalidos.csv ({len(gastos_quar)} filas)

   Output:
   └─ {OUT}/
      ├─ ut1.db (SQLite + vistas)
      └─ reporte.md
""")
