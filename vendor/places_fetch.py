import requests
import json
from config import API_KEY, SEARCH_RADIUS

def fetch_vendors(lat, lng, keyword):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        "location": f"{lat},{lng}",
        "radius": SEARCH_RADIUS,
        "keyword": keyword,
        "key": API_KEY
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print("API request failed with status:", response.status_code)
        return []
        
    data = response.json()
    
    if data.get("status") != "OK":
        print("API responded with status:", data.get("status"))
        if "error_message" in data:
            print("Error message:", data["error_message"])
        return []
        
    return data.get("results", [])

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)