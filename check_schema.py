from shared.supabase_client import get_supabase_client

def print_table_schema(table_name):
    supabase = get_supabase_client()
    result = supabase.table(table_name).select("*").limit(1).execute()
    if result.data:
        print("Columns:", result.data[0].keys())
    else:
        print("Table is empty, so schema can't be listed here. Check the Supabase dashboard.")

if __name__ == "__main__":
    print_table_schema("meals")
