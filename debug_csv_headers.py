import csv
from pathlib import Path

CSV_PATH = Path("myfitnesspal-reports/comidas.csv")

with CSV_PATH.open(newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    print("Detected Headers:", reader.fieldnames)
