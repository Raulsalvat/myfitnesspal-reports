# shared/test_env.py

import os
from dotenv import load_dotenv

load_dotenv()

print("✅ SUPABASE_URL:", os.getenv("SUPABASE_URL"))
print("✅ SUPABASE_KEY:", os.getenv("SUPABASE_KEY")[:10] + "..." if os.getenv("SUPABASE_KEY") else "❌ No KEY")
print("✅ OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY")[:10] + "..." if os.getenv("OPENAI_API_KEY") else "❌ No API KEY")
