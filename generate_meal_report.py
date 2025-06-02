# generate_meal_report.py

import os
from dotenv import load_dotenv
from supabase import create_client
from openai import OpenAI
from datetime import datetime
import csv

# Carga las variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializa Supabase y OpenAI
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
openai = OpenAI(api_key=OPENAI_API_KEY)

# Lee los datos del archivo CSV más reciente en la carpeta
csv_files = [f for f in os.listdir() if f.endswith('.csv')]
if not csv_files:
    print("❌ No se encontró ningún archivo CSV.")
    exit()

latest_file = max(csv_files, key=os.path.getctime)
with open(latest_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

# Prepara los datos para el prompt
meal_data = "\n".join([", ".join(row) for row in rows])

# Llama al modelo OpenAI
prompt = f"""Actúa como nutricionista experto. Analiza los siguientes datos de comida:
{meal_data}

Genera un informe claro y educativo, con puntos destacados como resumen calórico, evaluación de macronutrientes y recomendaciones saludables para mejorar la dieta."""

completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

report_text = completion.choices[0].message.content.strip()
date_range = f"{rows[1][0]} → {rows[-1][0]}"  # Suponiendo que la fecha está en la primera columna
summary = "Resumen nutricional generado automáticamente."

# Guarda el informe en Supabase
data = {
    "date_range": date_range,
    "summary": summary,
    "report": report_text,
    "report_type": "nutrition"
}

supabase.table("reports").insert(data).execute()

# Muestra el informe
print("🧾 Informe generado:")
print(report_text)
