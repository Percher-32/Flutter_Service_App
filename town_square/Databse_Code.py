import supabase
import json
from urllib.request import urlopen
from pydantic import BaseModel
import geopy
import geocoder

url: str = "http://127.0.0.1:54321"
key: str = "sb_publishable_ACJWlzQHlZjBrEguHvfOxg_3BJgxAaH"


# Initialize the client
supabase = supabase.create_client(url, key)

bussiness_database_name = "[Beta]Business"
bussiness_location_database_name = "[Beta]Business_Location"
user_database_name = "[Beta]User"



def add_bussines(user_name,name,website = None,email = None,links = None,location = None):
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
    
    response = supabase.table(user_database_name).update({"Business_Id":bussines_id}).eq({"username":user_name}).execute()
    
    
    print(f"Sent {bussiness_database_name} Data : \n{response.data}\n")
    
    return bussines_id
    
def add_business_location(business_id,location:tuple):
    data = {
        "Business_Id":business_id,
        "Location" : f"POINT({location[0]} {location[1]})"
    }
    
    

    response = supabase.table(bussiness_location_database_name).insert(data).execute()
    
    
    
    print(f"Sent {bussiness_location_database_name} Data : \n{response.data}\n")

def get_user_data(user_name):
    response = supabase.table(user_database_name).select("*").eq("username", user_name).execute()
    if len(response.data) :
        return response.data[0]
    else:
        return False
    
    
def add_user(user_name:str,hashword:str,type = "User",email = None,full_name = None,business_id = None):
    data = {
        "username":user_name,
        "hashword" : hashword,
        "type" : type,
        "email":email,
        "Full_Name":full_name,
        "Business_Id":business_id
    }
    
    

    response = supabase.table(user_database_name).insert(data).execute()
    
    print(response.data)
    

    
    
# add_user("Marty","LALALALGA",email="nogat@gmail.com")
ans = get_user_data("Martyx")

print(ans)
    
    
    
    



