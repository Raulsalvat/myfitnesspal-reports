from supabase_client import get_supabase_client
from config import TABLE_NAME

def read_meals():
    supabase = get_supabase_client()
    response = supabase.table(TABLE_NAME).select("*").order("date", desc=False).execute()

    if response.data:
        print("📋 Meals from Supabase:\n")
        for row in response.data:
            print(f"{row['date']} - {row['meal']} at {row['time']} | {row['calories']} kcal")
    else:
        print("⚠️ No data found in the 'meals' table.")

if __name__ == "__main__":
    read_meals()
