import csv
from pathlib import Path
from shared.supabase_client import get_supabase_client

CSV_PATH = Path("myfitnesspal-reports/comidas.csv")

# Map human-readable CSV headers to Supabase field names
HEADER_MAP = {
    "Date": "date",
    "Meal": "meal",
    "Time": "time",
    "Calories": "calories",
    "Fat (g)": "fat_g",
    "Saturated Fat": "saturated_fat",
    "Polyunsaturated Fat": "polyunsaturated_fat",
    "Monounsaturated Fat": "monounsaturated_fat",
    "Trans Fat": "trans_fat",
    "Cholesterol": "cholesterol",
    "Sodium (mg)": "sodium_mg",
    "Potassium": "potassium",
    "Carbohydrates (g)": "carbohydrates_g",
    "Fiber": "fiber",
    "Sugar": "sugar",
    "Protein (g)": "protein_g",
    "Vitamin A": "vitamin_a",
    "Vitamin C": "vitamin_c",
    "Calcium": "calcium",
    "Iron": "iron",
    "Note": "note"
}

def load_csv_to_supabase():
    supabase = get_supabase_client()

    with CSV_PATH.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            record = {}
            for header, value in row.items():
                field = HEADER_MAP.get(header)
                if not field:
                    continue
                if value in (None, "", "null"):
                    record[field] = None
                elif field in ("date", "meal", "time", "note"):
                    record[field] = value
                else:
                    try:
                        record[field] = float(value)
                    except ValueError:
                        record[field] = None
            if not record.get("date") or not record.get("meal") or not record.get("calories"):
                print("⏭️ Skipping invalid or empty row")
                continue
            print("Inserting:", record)
            supabase.table("meals").insert(record).execute()

if __name__ == "__main__":
    load_csv_to_supabase()
