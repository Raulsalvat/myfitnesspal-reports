import streamlit as st
import pandas as pd
import os
from reports.nutrition.generate import main as generar_informe

# Título
st.title("📊 Informe de Comidas - MyFitnessPal")

# Instrucciones
st.markdown("""
### 📝 Instrucciones:
1. Entra a la app de **MyFitnessPal** y exporta tu diario como **CSV**.
2. Sube el archivo aquí.
3. Espera unos segundos mientras se genera tu informe.
4. ✅ El informe se guarda automáticamente en Supabase para futuras consultas.
""")

# Subida de archivo
uploaded_file = st.file_uploader("📁 Sube tu archivo CSV de comidas", type=["csv"])

if uploaded_file:
    with open("comidas.csv", "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ Archivo subido correctamente.")

    with st.spinner("🧠 Generando informe..."):
        try:
            generar_informe()
            st.success("✅ Informe generado y guardado en Supabase.")
        except Exception as e:
            st.error(f"❌ Error al generar el informe: {str(e)}")
