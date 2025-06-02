from supabase_client import get_supabase_client
from config import TABLE_NAME
from analyze_mfp import process_myfitnesspal_csv
import pandas as pd  # Asegúrate de tener pandas importado

def insert_meals():
    supabase = get_supabase_client()
    df = process_myfitnesspal_csv()

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        # Buscar si ya existe una comida igual
        existing = supabase.table(TABLE_NAME).select("id").match({
            "date": str(row["date"]),
            "meal": row["meal"],
            "time": row["time"],
            "calories": row["calories"]
        }).execute()

        if not existing.data:
            # Convertir la fila en diccionario, reemplazar NaN por None
            data = row.where(pd.notnull(row), None).to_dict()
            data["date"] = str(data["date"])  # Supabase requiere string para fecha

            supabase.table(TABLE_NAME).insert(data).execute()
            inserted += 1
        else:
            print(f"⚠️ Ya existe: {row['date']} - {row['meal']} - {row['time']}")
            skipped += 1

    print(f"\n✅ Nuevos insertados: {inserted}")
    print(f"⏭️ Duplicados saltados: {skipped}")
