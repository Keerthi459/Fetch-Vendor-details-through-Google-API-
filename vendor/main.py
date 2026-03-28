from geocode import get_coordinates
from places_fetch import fetch_vendors
from data_clean import clean_vendors
from utils import save_json
from config import VENDOR_TYPES
from ranking import process_vendors

# Step 1: Get coordinates
lat, lng = get_coordinates("Madurai, Tamil Nadu")
print("Coordinates:", lat, lng)

# Step 2: Fetch vendors by type
all_vendors = []

for vtype in VENDOR_TYPES:
    print(f"\nFetching: {vtype}")
    vendors = fetch_vendors(lat, lng, vtype)

    if not vendors:
        print("⚠ No results OR API blocked")

    for v in vendors:
        print(v["name"], "-", v.get("vicinity"))

    all_vendors.extend(vendors)

print("\nTotal raw vendors:", len(all_vendors))

# Step 3: Clean data
cleaned_vendors = clean_vendors(all_vendors)

# Step 4: Rank the vendors
ranked_vendors = process_vendors(cleaned_vendors)

# Step 5: Save
save_json(ranked_vendors, "output/vendors.json")

print("Saved → output/vendors.json")
print("Total valid, ranked vendors:", len(ranked_vendors))