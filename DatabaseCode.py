import supabase

# Replace these with the values from 'npx supabase status'
url: str = "http://127.0.0.1:54321"
key: str = "sb_publishable_ACJWlzQHlZjBrEguHvfOxg_3BJgxAaH"

# Initialize the client
supabase = supabase.create_client(url, key)

try:
    response = supabase.table("Beta").select("*").execute()
    print("Successfully connected!")
    print("Data:", response.data)
except Exception as e:
    print(f"Error connecting: {e}")