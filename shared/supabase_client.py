# shared/supabase_client.py

"""
Centraliza la conexión con Supabase.
Carga las credenciales desde un archivo .env y crea un cliente reutilizable.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno desde .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validación básica por si faltan claves
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("⚠️ Las variables SUPABASE_URL o SUPABASE_KEY no están definidas en el archivo .env")

# Crear el cliente Supabase (tipo Client para autocompletado)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
