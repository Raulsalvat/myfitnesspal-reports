# fetch_past_reports.py

import os
from dotenv import load_dotenv
from supabase import create_client

# Cargar claves desde .env
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Conexión con Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Menú interactivo
print("🔎 ¿Qué tipo de informe deseas consultar?")
print("1. nutrition")
print("2. workout")
print("3. habit")
print("4. motivation")
print("5. todos")

choice = input("Elige una opción (1-5): ").strip()

types = {
    "1": "nutrition",
    "2": "workout",
    "3": "habit",
    "4": "motivation",
    "5": None
}

filter_type = types.get(choice)

# Consulta dinámica
query = supabase.table("reports").select("*").order("created_at", desc=True)
if filter_type:
    query = query.eq("report_type", filter_type)

response = query.execute()

print("\n🧪 DEBUG - Datos crudos desde Supabase:")
print(response.data)

reports = response.data


# Resultado
if not reports:
    print("\n📭 No hay informes guardados para este tipo.")
else:
    print("\n📑 Resultados encontrados:")
    for report in reports:
        print("🗓️  Fecha:", report.get("date_range", "—"))
        print("📌 Tipo:", report.get("report_type", "—"))
        print("📝 Resumen:", report.get("summary", "—"))
        print("📄 Informe completo:\n", report.get("report", "—"))
        print("=" * 80)
