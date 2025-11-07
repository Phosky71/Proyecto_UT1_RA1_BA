"""
Copia el reporte generado a la carpeta site/content/reportes/
para publicación con Quartz
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "output" / "reporte.md"
TARGET_DIR = ROOT.parent / "site" / "content" / "reportes"
TARGET_DIR.mkdir(parents=True, exist_ok=True)
TARGET = TARGET_DIR / "reporte-finanzas-UT1.md"

if SOURCE.exists():
    shutil.copy2(SOURCE, TARGET)
    print(f"✓ Copiado: {SOURCE}")
    print(f"  → {TARGET}")
else:
    print(f"✗ No encontrado: {SOURCE}")
    print("  Ejecuta primero: python project/ingest/run.py")
