from places_fetch import fetch_photo_studios

vendors = fetch_photo_studios("Madurai Tamil Nadu")

for v in vendors:
    print(v)

print("Total vendors:", len(vendors))