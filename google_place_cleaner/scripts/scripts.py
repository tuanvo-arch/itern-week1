import json 
import pandas as pd

# Xử lý dữ liệu thiếu trong cột 'user_ratings_total'
def handle_missing_data(df):
    if "user_ratings_total" in df.columns:
        df["user_ratings_total"] = df["user_ratings_total"].fillna(0).astype(int)
    return df

# Xử lý cột 'types' để lấy giá trị đầu tiên nếu là danh sách
def process_types(x):
    if isinstance(x, list):
        return str(x[0])
    if isinstance(x, str):
        return x
    return "Unknown"

# Chuẩn hóa và làm sạch dữ liệu
def normalize_and_clean_data(df):
    df.rename(
        columns={
            "geometry.location.lat": "latitude",
            "geometry.location.lng": "longitude",
        }, inplace=True
    )
    wanted_columns = ["place_id", "name", "rating", "user_ratings_total", "latitude", "longitude", "address", "types"]
    
    final_columns = [c for c in wanted_columns if c in df.columns]
    final_df = df[final_columns].copy()
    
    return final_df

# Lấy và xử lý dữ liệu đánh giá từ
def get_reviews_data(json_data):
    try:
        if not json_data:
            return pd.DataFrame()  
        
        reviews_df = pd.json_normalize(
            json_data,
            record_path=["reviews"],
            meta=["place_id", "name"],
            meta_prefix="place_",
            errors='ignore'
        )
        
        if reviews_df.empty:
            print("no data")
            return pd.DataFrame()
        
        reviews_df.rename(
            columns={
                "name": "author_name",
                "rating": "review_rating",
                "text": "review_text",
                "time": "review_time"
            }, inplace=True
        )
        
        wanted_review_columns = ["author_name", "review_rating", "review_text", "review_time"]
        final_cols = [c for c in wanted_review_columns if c in reviews_df.columns]
        reviews_df = reviews_df[final_cols]
        if "review_text" in reviews_df.columns:
            reviews_df["review_text"] = reviews_df["review_text"].fillna("No text review").astype(str)
        return reviews_df
    
    except Exception as e:
        print(f"Lỗi khi lưu dữ liệu: {e}")
        return pd.DataFrame()
    

if __name__ == "__main__":
    with open("../data_raw/locations_raw.json", "r", encoding="utf-8") as f:
        place = json.load(f)
    
    place_df = pd.json_normalize(place)
    
    place_df = handle_missing_data(place_df)
    
    if "types" in place_df.columns:
        place_df["types"] = place_df["types"].apply(process_types)
    
    final_df = normalize_and_clean_data(place_df)
    reviews_df = get_reviews_data(place)
    
    final_df.to_csv("../output/locations_cleaned.csv", encoding="utf-8", index=False)
    print(place_df.head())
    
    reviews_df.to_csv("../output/reviews_cleaned.csv", encoding="utf-8", index=False)
    print(reviews_df.head())