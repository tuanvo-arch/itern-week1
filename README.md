README – Week 1 Mini Task

Intern: Võ Đức Tuân
Ngày hoàn thành & nộp: 28/11/2025
Thời gian thực hiện: 5 ngày

Mục tiêu công ty (đã đạt 100%)
Python script: đọc file JSON Google Places → xử lý missing → trích lat/lng → xuất cleaned_locations.csv
SQL (SQLite): dùng Window Function (RANK / DENSE_RANK) để xếp hạng địa điểm theo rating trong từng type

1. Cấu trúc dự án:
# Cấu trúc dự án
```
WEEK01/
└── google_place_cleaner/
    ├── data_raw/
    │   └── locations_raw.json      dữ liệu thô từ Google Places API
    ├── notebooks/
    ├── output/
    │   ├── locations_cleaned.csv   file CSV sạch (yêu cầu chính)
    │   └── reviews_cleaned.csv
    ├── scripts/
    │   ├── crawler.py              script crawl tự động bằng Apify
    │   └── clean_places.py         script làm sạch + xuất CSV
    ├── env/
    ├── sqlite_demo/
    │   ├── demodb.db
    │   └── demodb.sqbpro           PROJECT DB Browser
    └── README.md
```
2. Cách chạy toàn bộ project:

# Bước 1: Crawl dữ liệu mới bằng Apify
    Chỉ chạy khi muốn lấy dữ liệu mới
    python scripts/crawler.py
    → Tự động lưu vào data_raw/locations_raw.json

# Bước 2: Làm sạch + tạo file CSV
    python scripts/clean_places.py
    → tạo 2 file CSV sạch

# Bước 3: Import dữ liệu vào DB Browser 

3. Hướng dẫn mở dự án SQLite
### Mở project SQLite
Double-click file `sqlite_demo\demodb.sqbpro` bằng DB Browser for SQLite → tất cả bảng + query sẵn sàng chạy ngay.
(Tải DB Browser: https://sqlitebrowser.org)

Võ Đức Tuân
Slack/Email: tuan.vo@kyanon.digital
