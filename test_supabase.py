from shared.supabase_client import get_supabase_client

def main():
    supabase = get_supabase_client()
    response = supabase.table("meals").select("*").limit(5).execute()
    for entry in response.data:
        print(entry)

if __name__ == "__main__":
    main()
