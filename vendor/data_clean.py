def clean_vendors(vendor_list, min_rating=3, min_reviews=5):
    cleaned = []
    for v in vendor_list:
        rating = v.get("rating", 0)
        reviews = v.get("user_ratings_total", 0)
        if rating >= min_rating and reviews >= min_reviews:
            cleaned.append({
                "name": v.get("name"),
                "address": v.get("vicinity"),
                "rating": rating,
                "reviews": reviews
            })
    return cleaned
