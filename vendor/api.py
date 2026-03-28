import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os

from geocode import get_coordinates
from places_fetch import fetch_vendors
from data_clean import clean_vendors
from ranking import process_vendors
from utils import save_json

app = FastAPI(title="Vendor Directory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_FILE = "output/vendors.json"

@app.get("/vendors")
def get_vendors(
    location: str = Query(default="Madurai, Tamil Nadu"),
    service: str = Query(default="studio")
):
    try:
        # Step 1: Get coordinates
        lat, lng = get_coordinates(location)
        
        # Step 2: Fetch vendors for the specific service
        vendors = fetch_vendors(lat, lng, service)
        
        if not vendors:
            return []
            
        # Step 3: Clean data
        cleaned_vendors = clean_vendors(vendors)
        
        # Step 4: Rank the vendors
        ranked_vendors = process_vendors(cleaned_vendors)
        
        # Step 5: Save for logging purposes (optional)
        save_json(ranked_vendors, OUTPUT_FILE)
        
        return ranked_vendors
    except Exception as e:
        print(f"Error fetching vendors: {e}")
        return []

