import pandas as pd
import json
from apify_client import ApifyClient

API_TOKEN = ""

SEARCH_KEYWORDS = [
    "Highlands Coffee District 1",
    "Pizza 4P's Ho Chi Minh",
    "Bitexco Financial Tower",
    "Ben Thanh Market",
    "Gem Center District 1"
]
MAX_PLACES_PER_KEYWORD = 10
MAX_REVIEWS = 5

def fetch_data_from_apify():
    client = ApifyClient(API_TOKEN)
    
    run_input = {
        "searchStringsArray": SEARCH_KEYWORDS,        
        "maxCrawledPlacesPerSearch": MAX_PLACES_PER_KEYWORD,
        "language": "vi",
        "maxReviews": MAX_REVIEWS,
        "scrapeReviewerName": True,
        "reviewsSort": "newest",
        "zoom": 15
    }
    
    print(f"Starting the Apify actor for {len(SEARCH_KEYWORDS)} keywords...")
    run = client.actor("compass/crawler-google-places").call(run_input=run_input)
    
    print("Done crawler, fetching dataset...")
    dataset_items = client.dataset(run["defaultDatasetId"]).iterate_items()
    
    return list(dataset_items)

def transform_data(apify_items):
    cleaned_data = []
    
    for item in apify_items:
        categories_list = item.get("categories")
        if not categories_list:
            cat_name = item.get("categoryName")
            categories_list = [cat_name] if cat_name else []

        place = {
            "place_id": item.get("placeId") or item.get("cid"),
            "name": item.get("title"),
            "search_string": item.get("searchString"),
            "rating": item.get("totalScore"),
            "user_ratings_total": item.get("reviewsCount"),
            "geometry": {
                "location":{
                "lat": item.get("location", {}).get("lat"),
                "lng": item.get("location", {}).get("lng"),
            },},
            "address": item.get("address"),
            "types": categories_list,
            "reviews": []
        }
        
        if "reviews" in item:
            for rev in item["reviews"]:
                place["reviews"].append({
                    "name": rev.get("name"),
                    "rating": rev.get("stars"),
                    "text": rev.get("text"),
                    "time": rev.get("publishedAtDate"),
                })
        
        cleaned_data.append(place)
    
    return cleaned_data

if __name__ == "__main__":
    raw_data = fetch_data_from_apify()
    final_data = transform_data(raw_data)
    
    try:
        with open("../data_raw/locations_raw.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"Đã lưu {len(final_data)} địa điểm vào locations_raw.json")

        print("\nVí dụ các loại hình tìm được:")
        for p in final_data[:5]:
            print(f"- {p['name']}: {p['types']}")
            
    except Exception as e:
        print(f"Lỗi khi lưu file: {e}")