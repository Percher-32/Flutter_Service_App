import supabase
import json
from urllib.request import urlopen
import fastapi
import geopy
import geocoder

url: str = "http://127.0.0.1:54321"
key: str = "sb_publishable_ACJWlzQHlZjBrEguHvfOxg_3BJgxAaH"


# Initialize the client
supabase = supabase.create_client(url, key)

bussiness_database_name = "[Beta]Business"
bussiness_location_database_name = "[Beta]Business_Location"



def add_bussines(name,website = None,email = None,links = None,location = None):
    data = {
        "Name": name,
        "Website":website,
        "Email" : email,
        "Links" : links
    }



    response = supabase.table(bussiness_database_name).insert(data).execute()
    bussines_id = response.data[0]["id"]
    
    
    if location == None:
        loc_data = geocoder.ip('me').latlng
    else:
        loc_data = location
        
    add_business_location(bussines_id,loc_data)
    
    
    print(f"Sent {bussiness_database_name} Data : \n{response.data}\n")
    
def add_business_location(business_id,location:tuple):
    data = {
        "Business_Id":business_id,
        "Location" : f"POINT({location[0]} {location[1]})"
    }
    
    

    response = supabase.table(bussiness_location_database_name).insert(data).execute()
    
    
    
    print(f"Sent {bussiness_location_database_name} Data : \n{response.data}\n")
    
    
    
add_bussines("Mikes Ranch")



