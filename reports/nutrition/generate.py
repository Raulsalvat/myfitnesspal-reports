# reports/nutrition/generate.py

"""
Este script lee un archivo CSV con datos de comidas, genera un informe nutricional
usando un prompt definido, y guarda el resultado en Supabase.
"""

import sys
import os
import csv
from datetime import datetime

# ✅ Asegura que la raíz del proyecto esté en sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# 📦 Importaciones desde el módulo compartido
from shared.supabase_client import supabase
from shared.utils import format_date_range, truncate_text, print_divider

# 📄 CSV de entrada
CSV_FILE = "comidas.csv"

# 📄 Prompt base
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompt.txt")

# 🧠 OpenAI (versión moderna)
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_csv(filepath):
    if not os.path.exists(filepath):
        print("❌ No se encontró el archivo CSV:", filepath)
        return []

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def load_prompt():
    with open(PROMPT_PATH, encoding="utf-8") as f:
        return f.read()

def build_context(rows):
    if not rows:
        return "No hay datos disponibles."

    dates = sorted([r["fecha"] for r in rows])
    start, end = dates[0], dates[-1]

    resumen = ""
    comidas = {"desayuno": [], "almuerzo": [], "cena": []}
    for r in rows:
        tipo = r.get("comida", "").lower()
        if tipo in comidas:
            try:
                comidas[tipo].append(int(r.get("calorias", 0)))
            except ValueError:
                continue

    for comida, cal_list in comidas.items():
        avg = sum(cal_list) // len(cal_list) if cal_list else 0
        resumen += f"- {comida.title()}: {avg} kcal por día\n"

    return f"Rango de fechas: {format_date_range(start, end)}\nResumen calórico:\n{resumen.strip()}"

def generate_report(context, prompt_template):
    final_prompt = f"{prompt_template.strip()}\n\n{context}"
    print_divider("Prompt Final Enviado")
    print(truncate_text(final_prompt, 500))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": final_prompt}],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()

def save_report_to_supabase(date_range, summary, full_report):
    supabase.table("reports").insert({
        "report_type": "nutrition",
        "date_range": date_range,
        "summary": summary,
        "report": full_report
    }).execute()

    print("\n✅ Informe guardado en Supabase.")

def main():
    rows = load_csv(CSV_FILE)
    if not rows:
        return

    prompt_template = load_prompt()
    context = build_context(rows)
    report = generate_report(context, prompt_template)
    summary = truncate_text(report, 200)
    date_range = format_date_range(rows[0]["fecha"], rows[-1]["fecha"])

    print_divider("Informe Generado")
    print(report)

    save_report_to_supabase(date_range, summary, report)

if __name__ == "__main__":
    main()
