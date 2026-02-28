import supabase
import json
from pydantic import BaseModel
import geopy
import geocoder
from hashcode import *
import random
from shapely import wkb


url: str = "http://127.0.0.1:54321"
key: str = "sb_publishable_ACJWlzQHlZjBrEguHvfOxg_3BJgxAaH"


# Initialize the client
supabase = supabase.create_client(url, key)

bussiness_database_name = "[Beta]Business"
bussiness_location_database_name = "[Beta]Business_Location"
user_database_name = "[Beta]User"
service_database_name = "[Beta]Services"



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
    
    supabase.table(user_database_name).update({"Business_Id":bussines_id}).eq("email",user_name).execute()
    supabase.table(user_database_name).update({"type":"Owner"}).eq("email",user_name).execute()
    
    
    print(f"Sent {bussiness_database_name} Data : \n{response.data}\n")
    
    return response

def add_business_location(business_id,location:tuple):
    data = {
        "Business_Id":business_id,
        "Location" : f"POINT({location[0]} {location[1]})"
    }
    
    

    response = supabase.table(bussiness_location_database_name).insert(data).execute()
    
    
    
    print(f"Sent {bussiness_location_database_name} Data : \n{response.data}\n")

def get_services_from_business(business_id):
    resp = supabase.table(service_database_name).select("id").eq("business_id",business_id).execute()
    
    return resp.data
    



def add_service_to_business(business_id,name:str,pay_type = "PayOnDay",gotoloc = 1,customaddons = {},scheduled = 0):
    data = {
        "business_id":business_id,
        "Name":name,
        "Pay_type":pay_type,
        "GotoLoc":gotoloc,
        "Custom_Addons":customaddons,
        "Scheduled?" : scheduled
    }
    
    
    reponse = supabase.table(service_database_name).insert(data).execute()
    
    return reponse


    
    
    
    





def get_user_data(user_name):
    response = supabase.table(user_database_name).select("*").eq("email", user_name).execute()
    
    hex_data = response.data[0]["Location"]
    
    if not hex_data == None:
        point = wkb.loads(hex_data, hex=True)
        loclist = list(point.coords[0])
        response.data[0]["Location"] = loclist

    
    if len(response.data) :
        return response.data[0]
    else:
        return False
    
def add_user(email:str,password:str,type = "User",full_name = None,business_id = None,location : tuple = None):
    if location == None:
        location = (0,0)
    data = {
        "hashword" : get_password_hash(password),
        "type" : type,
        "email":email,
        "Full_Name":full_name,
        "Business_Id":business_id,
        "Location" : f"POINT({location[0]} {location[1]})"
    }
    
    

    response = supabase.table(user_database_name).insert(data).execute()
    
    print(response.data)
    
    return response.data[0]
    
def add_completed_service_to_user(user_data,service_id):
    data = user_data
    email = data["email"]
    
    all_serivices : list = data["Services_Done"]
    
    all_serivices.append(service_id)
    
    
    supabase.table(user_database_name).update({"Services_Done":all_serivices}).eq("email",email).execute()

def add_new_favorite_service_to_user(user_data,service_id):
    data = user_data
    
    email = data["email"]
    
    all_serivices : list = data["Favorite_Services"]
    
    all_serivices.append(service_id)
    
    
    supabase.table(user_database_name).update({"Favorite_Services":all_serivices}).eq("email",email).execute()
    
    
    
if __name__ == "__main__":
    busid = get_user_data("Lincoln2@gmail.com")["Business_Id"]
    for i in range(50):
        add_business_location(busid,(random.random() * 50,random.random() * 50))
    # print(get_services_from_business(business_id=busid))



# ax = get_user_data("Lincoln")




