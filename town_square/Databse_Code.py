import supabase
import json
from pydantic import BaseModel
import geopy
import geocoder
from hashcode import *
from shapely import wkb


url: str = "http://127.0.0.1:54321"
key: str = "sb_publishable_ACJWlzQHlZjBrEguHvfOxg_3BJgxAaH"


# Initialize the client
supabase = supabase.create_client(url, key)

bussiness_database_name = "[Beta]Business"
bussiness_location_database_name = "[Beta]Business_Location"
user_database_name = "[Beta]User"



myloc = geocoder.ip('me').latlng



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
        loc_data = (0,0)
    else:
        loc_data = location
        
    add_business_location(bussines_id,loc_data)
    
    supabase.table(user_database_name).update({"Business_Id":bussines_id}).eq("username",user_name).execute()
    supabase.table(user_database_name).update({"type":"Owner"}).eq("username",user_name).execute()
    
    
    print(f"Sent {bussiness_database_name} Data : \n{response.data}\n")
    
    return response



    
def add_business_location(business_id,location:tuple):
    data = {
        "Business_Id":business_id,
        "Location" : f"POINT({location[0]} {location[1]})"
    }
    
    

    response = supabase.table(bussiness_location_database_name).insert(data).execute()
    
    
    
    print(f"Sent {bussiness_location_database_name} Data : \n{response.data}\n")

def get_user_data(user_name):
    response = supabase.table(user_database_name).select("*").eq("username", user_name).execute()
    
    hex_data = response.data[0]["Location"]
    
    if not hex_data == None:
        point = wkb.loads(hex_data, hex=True)
        loclist = list(point.coords[0])
        response.data[0]["Location"] = loclist

    
    if len(response.data) :
        return response.data[0]
    else:
        return False
    
    
def add_user(user_name:str,password:str,type = "User",email = None,full_name = None,business_id = None,location : tuple = None):
    if location == None:
        location = (0,0)
    data = {
        "username":user_name,
        "hashword" : get_password_hash(password),
        "type" : type,
        "email":email,
        "Full_Name":full_name,
        "Business_Id":business_id,
        "Location" : f"POINT({location[0]} {location[1]})"
    }
    
    

    response = supabase.table(user_database_name).insert(data).execute()
    
    print(response.data)
    
def add_service_done(user_name,service_id):
    data = get_user_data(user_name)
    
    all_serivices : list = data["Services_Done"]
    
    all_serivices.append(service_id)
    
    
    supabase.table(user_database_name).update({"Services_Done":all_serivices}).eq("username",user_name).execute()
    
    

    
# add_user("Lincoln","ABC123",location=myloc)
add_service_done("Lincoln",45)
# add_bussines("Lincoln","LR studios",website="www.Lincoln.org.uk",email="Aroundtheworld@gmail.com")



# ax = get_user_data("Lincoln")




