# 📊 MyFitnessPal Reports

App para subir archivos CSV de comidas y generar informes nutricionales usando IA con OpenAI y Supabase.

---

## 🚀 Características

- Subida de archivos CSV exportados desde MyFitnessPal
- Generación de informes nutricionales por día
- Clasificación por tipo de comida (desayuno, comida, cena, snacks)
- Análisis de nutrientes clave con OpenAI
- Almacenamiento y recuperación de datos vía Supabase

---

## 🛠️ Requisitos

- Python 3.10 o superior
- Git
- Cuenta en [OpenAI](https://platform.openai.com/)
- Proyecto en [Supabase](https://supabase.com/)

---

## 🔐 Configuración del entorno

Crea un archivo `.env` en la raíz del proyecto (no se sube a GitHub gracias al `.gitignore`) con el siguiente contenido:

```env
OPENAI_API_KEY=tu_clave_de_openai
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_clave_service_role_de_supabase
DEBUG=True
PORT=5000
