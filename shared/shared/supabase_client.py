# shared/supabase_client.py

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("⚠️ Las variables SUPABASE_URL o SUPABASE_KEY no están definidas en el archivo .env")

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)
