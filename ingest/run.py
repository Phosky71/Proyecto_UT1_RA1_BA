"""
Pipeline finanzas: presupuesto vs gasto (ETL ligero)

Bronce → Plata → Oro → Quarantine → Reporte

"""

import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data" / "drops"
STORAGE = ROOT / "data" / "storage"
BRONZE = STORAGE / "bronze"
SILVER = STORAGE / "silver"
GOLD = STORAGE / "gold"
QUARANTINE = ROOT / "data" / "quarantine"
OUT = ROOT / "output"
SQL = ROOT / "sql"

for folder in [BRONZE, SILVER, GOLD, QUARANTINE, OUT]:
    folder.mkdir(parents=True, exist_ok=True)

# ========== INGESTA 1) LECTURA DESDE CSV ==========
print("=" * 70)
print("RETO 1: INGESTIÓN - BRONZE (RAW)")
print("=" * 70)
presupuesto_csv = DATA / "presupuesto.csv"
gastos_csv = DATA / "gastos.csv"
raw_gastos, raw_presup = [], []
utcnow = datetime.now(timezone.utc).isoformat()


def compute_batch_id(name, df_len):
    # Usar nombre y tamaño
    content = f"{name}_{df_len}_{utcnow}"
    return hashlib.md5(content.encode()).hexdigest()[:16]


if gastos_csv.exists():
    df = pd.read_csv(gastos_csv, encoding="utf-8")
    df["_source_file"] = gastos_csv.name
    df["_ingest_ts"] = utcnow
    df["_batch_id"] = compute_batch_id(gastos_csv.name, len(df))
    raw_gastos.append(df)
    print(f"✓ Ingesta: {gastos_csv.name} → batch_id={df['_batch_id'].iloc[0]}")

if presupuesto_csv.exists():
    df = pd.read_csv(presupuesto_csv, encoding="utf-8")
    df["_source_file"] = presupuesto_csv.name
    df["_ingest_ts"] = utcnow
    df["_batch_id"] = compute_batch_id(presupuesto_csv.name, len(df))
    raw_presup.append(df)
    print(f"✓ Ingesta: {presupuesto_csv.name} → batch_id={df['_batch_id'].iloc[0]}")

gastos_raw = pd.concat(raw_gastos, ignore_index=True) if raw_gastos else pd.DataFrame()
presup_raw = pd.concat(raw_presup, ignore_index=True) if raw_presup else pd.DataFrame()

# Guardar en BRONZE (solo Parquet)
gastos_raw.to_parquet(BRONZE / "gastos_raw.parquet", index=False)
presup_raw.to_parquet(BRONZE / "presupuesto_raw.parquet", index=False)

print(f"\n✓ Bronze guardado: {BRONZE}")
print(f" - gastos_raw.parquet: {len(gastos_raw)} filas")
print(f" - presupuesto_raw.parquet: {len(presup_raw)} filas")

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
    if pd.isna(area):
        return None
    clean = str(area).strip().lower()
    return AREAS_MAP.get(clean, str(area).strip().title())


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

presup_clean.to_parquet(SILVER / "presupuesto_clean.parquet", index=False)
gastos_clean.to_parquet(SILVER / "gastos_clean.parquet", index=False)
if not presup_quar.empty:
    presup_quar.to_parquet(QUARANTINE / "presupuesto_invalidos.parquet", index=False)
if not gastos_quar.empty:
    gastos_quar.to_parquet(QUARANTINE / "gastos_invalidos.parquet", index=False)

# ========== 3) ORO: GOLD + ANALYTICS ==========
print("\n" + "=" * 70)
print("RETO 3: ORO - GOLD (ANALYTICS)")
print("=" * 70)

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
    kpi_df.to_parquet(GOLD / "kpi_ejecucion.parquet", index=False)

    area_agg = kpi_df.groupby("area", as_index=False).agg({
        "presupuesto": "sum",
        "gasto_acumulado": "sum",
        "presupuesto_restante": "sum"
    })
    area_agg["porcentaje_ejecucion"] = (area_agg["gasto_acumulado"] / area_agg["presupuesto"] * 100).round(2)
    area_agg.to_parquet(GOLD / "ejecucion_por_area.parquet", index=False)
else:
    kpi_df = pd.DataFrame()
    area_agg = pd.DataFrame()

# ========== 4) ALMACENAMIENTO: SQLITE ==========
print("\n" + "=" * 70)
print("ALMACENAMIENTO: SQLITE + VISTAS")
print("=" * 70)

sqlite_path = OUT / "finanzas.db"
conn = sqlite3.connect(sqlite_path)
kpi_df.to_sql("kpi_ejecucion", conn, if_exists="replace", index=False)
area_agg.to_sql("ejecucion_por_area", conn, if_exists="replace", index=False)
conn.commit()
conn.close()
print(f"✓ SQLite guardado: {sqlite_path}")

# ========== 5) REPORTE MARKDOWN ==========
print("\n" + "=" * 70)
print("RETO 4: REPORTE MARKDOWN")
print("=" * 70)

if (GOLD / "kpi_ejecucion.parquet").exists():
    kpi_rep = pd.read_parquet(GOLD / "kpi_ejecucion.parquet")
    area_rep = pd.read_parquet(GOLD / "ejecucion_por_area.parquet")
else:
    kpi_rep = kpi_df
    area_rep = area_agg

if not kpi_rep.empty:
    total_presup = kpi_rep["presupuesto"].sum()
    total_gasto = kpi_rep["gasto_acumulado"].sum()
    total_restante = total_presup - total_gasto
    ejecucion_global = (total_gasto / total_presup * 100) if total_presup > 0 else 0
    top_partidas = kpi_rep.sort_values("porcentaje_ejecucion", ascending=False).head(10)
    riesgo = kpi_rep[kpi_rep["porcentaje_ejecucion"] > 80].sort_values("porcentaje_ejecucion", ascending=False)
    # Tendencia mensual
    gastos_temp = pd.read_parquet(SILVER / "gastos_clean.parquet")
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

reporte = f"""# Ejecución Presupuestaria vs Gasto — Periodo {periodo}

**Informe de Análisis Financiero**

---

## 📊 Resumen Ejecutivo

| Métrica                | Valor           |
|------------------------|-----------------|
| **Presupuesto Total**  | {total_presup:,.2f} € |
| **Gasto Acumulado**    | {total_gasto:,.2f} € |
| **Presupuesto Restante** | {total_restante:,.2f} € |
| **% Ejecución Global** | {ejecucion_global:.2f}%    |

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

{area_rep.to_markdown(index=False, floatfmt='.2f') if not area_rep.empty else '*No hay datos disponibles*'}

---

## 🔝 Top 10 Partidas por Ejecución

{top_partidas[['area', 'partida', 'presupuesto', 'gasto_acumulado', 'porcentaje_ejecucion']].to_markdown(index=False, floatfmt='.2f') if not top_partidas.empty else '*No hay datos disponibles*'}

---

## ⚠️ Áreas en Riesgo (>80% Ejecución)

{riesgo[['area', 'partida', 'presupuesto', 'gasto_acumulado', 'presupuesto_restante', 'porcentaje_ejecucion']].to_markdown(index=False, floatfmt='.2f') if not riesgo.empty else '*No hay áreas en riesgo actualmente*'}

---

## 📅 Tendencia Mensual

### Gasto por Área y Mes (€)

{mensual_pivot.to_markdown(floatfmt='.2f') if not mensual_pivot.empty else '*No hay datos de tendencia mensual*'}

---

## 📋 Detalle Completo: Todas las Partidas

{kpi_rep[['area', 'partida', 'presupuesto', 'gasto_acumulado', 'presupuesto_restante', 'porcentaje_ejecucion']].to_markdown(index=False, floatfmt='.2f') if not kpi_rep.empty else '*No hay datos disponibles*'}

---

## 📌 Contexto del Informe

- **Periodo cubierto**: {periodo}
- **Última actualización**: {ultima_actualizacion}

---
"""

REPORTE_FILE = OUT / "reporte.md"
REPORTE_FILE.write_text(reporte, encoding="utf-8")

print(f"\n✓ Reporte generado: {REPORTE_FILE}")
print(f" {len(reporte)} caracteres")
