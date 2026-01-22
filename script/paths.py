from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

data_dir = project_root / "data"
db_dir = project_root / "db"

excel_file = data_dir / "DatabaseGranaroloFinal.xlsx"
db_file = db_dir / "Granarolo.db"

