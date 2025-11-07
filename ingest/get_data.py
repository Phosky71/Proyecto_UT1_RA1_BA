"""
Generador de datos de ejemplo para el caso 7: Finanzas
Crea gastos.csv y presupuesto.csv en project/data/drops/
"""
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DROPS = ROOT / "data" / "drops"
DROPS.mkdir(parents=True, exist_ok=True)

# Catálogo
AREAS = ["RRHH", "IT", "Marketing", "Ventas", "Operaciones"]
PARTIDAS = ["Personal", "Material", "Software", "Hardware", "Formacion", "Viajes", "Publicidad"]

# 1. Generar presupuesto.csv
presup_data = []
for area in AREAS:
    for partida in PARTIDAS:
        presup = random.randint(20000, 150000)
        presup_data.append({"area": area, "partida": partida, "presupuesto": presup})

df_presup = pd.DataFrame(presup_data)
df_presup.to_csv(DROPS / "presupuesto.csv", index=False)
print(f"✓ {DROPS / 'presupuesto.csv'} ({len(df_presup)} filas)")

# 2. Generar gastos.csv
gastos_data = []
start = datetime(2025, 1, 1)
for i in range(300):
    fecha = start + timedelta(days=random.randint(0, 300))
    area = random.choice(AREAS)
    partida = random.choice(PARTIDAS)
    # Buscar presupuesto correspondiente
    presup_row = df_presup[(df_presup["area"] == area) & (df_presup["partida"] == partida)]
    if not presup_row.empty:
        presup = presup_row.iloc[0]["presupuesto"]
        importe = random.uniform(100, presup * 0.1)
    else:
        importe = random.uniform(100, 5000)

    gastos_data.append({
        "fecha": fecha.strftime("%Y-%m-%d"),
        "area": area,
        "partida": partida,
        "importe": round(importe, 2)
    })

# Añadir datos de prueba para validación
# Área no normalizada
gastos_data.append({"fecha": "2025-03-15", "area": "  rrhh  ", "partida": "Personal", "importe": 1500.50})
# Partida inválida
gastos_data.append({"fecha": "2025-04-20", "area": "IT", "partida": "PartidaNoExiste", "importe": 2000.00})
# Importe negativo
gastos_data.append({"fecha": "2025-05-10", "area": "Marketing", "partida": "Publicidad", "importe": -500.00})
# Fecha inválida
gastos_data.append({"fecha": "2025-13-40", "area": "Ventas", "partida": "Viajes", "importe": 800.00})
# Duplicados para probar deduplicación
gastos_data.append({"fecha": "2025-06-15", "area": "IT", "partida": "Software", "importe": 3000.00})
gastos_data.append({"fecha": "2025-06-15", "area": "IT", "partida": "Software", "importe": 3500.00})

df_gastos = pd.DataFrame(gastos_data)
df_gastos.to_csv(DROPS / "gastos.csv", index=False)
print(f"✓ {DROPS / 'gastos.csv'} ({len(df_gastos)} filas)")
