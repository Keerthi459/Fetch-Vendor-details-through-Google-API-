import requests
from config import API_KEY

def get_coordinates(place_name):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": place_name,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "OK":
        raise Exception("Geocoding failed:", data["status"])

    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]
