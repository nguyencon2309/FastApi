import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Điền chuỗi kết nối MongoDB Atlas của bạn (đã thay pass và db name)
MONGODB_URL = os.getenv("MONGO_URL")  # Lấy từ biến môi trường trong .env của bạn

# Kết nối tới MongoDB Atlas
client = MongoClient(MONGODB_URL)
db = client["smart_tray"]  # Tên Database của bạn

# 2. Đọc file JSON xuất từ Firebase của bạn
# Giả sử file của bạn tên là 'firebase_data.json'
file = r'C:\Users\Admin\Downloads\data_firebase.json'
with open(file, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# --- HÀM CHUYỂN ĐỔI CẤU TRÚC FIREBASE -> MONGODB ---
def transform_firebase_data(firebase_group):
    """
    Biến đổi cấu trúc {"-OtKq7r...": {data}} thành danh sách [{data}, {data}]
    """
    mongo_documents = []
    if not firebase_group:
        return mongo_documents
        
    for firebase_key, food_data in firebase_group.items():
        # Copy lại dữ liệu để tránh ghi đè dữ liệu gốc
        doc = food_data.copy()
        
        # Firebase lưu ID làm Key, nếu trong data chưa có trường 'id' hoặc 'firebase_key' thì ta gán vào
        doc['firebase_key'] = firebase_key 
        
        mongo_documents.append(doc)
    return mongo_documents

# 3. Xử lý nhóm "food"
# Thay 'food' bằng chính xác Key nhóm 1 trong file JSON của bạn
if "food" in raw_data:
    print("Đang xử lý nhóm food...")
    food_list = transform_firebase_data(raw_data["food"])
    
    if food_list:
        collection_food = db["food"]  # Tạo collection tên là 'food'
        collection_food.drop()        # Xóa dữ liệu cũ nếu có để tránh trùng lặp khi chạy lại
        collection_food.insert_many(food_list)
        print(f" Successfully! Đã nạp {len(food_list)} món vào collection 'food'.")

# 4. Xử lý nhóm dữ liệu thứ 2 (bạn gọi là food_101)
# Thay 'food_101' bằng chính xác Key nhóm 2 trong file JSON của bạn
# (Ví dụ trong chuỗi của bạn có thể tên là 'food_101', 'food101'...)
# key_nhom_2 = "food_101" 

# if key_nhom_2 in raw_data:
#     print(f"Đang xử lý nhóm {key_nhom_2}...")
#     food101_list = transform_firebase_data(raw_data[key_nhom_2])
    
#     if food101_list:
#         collection_food101 = db["food101"]  # Tạo collection tên là 'food101'
#         collection_food101.drop()           # Xóa dữ liệu cũ nếu có
#         collection_food101.insert_many(food101_list)
#         print(f" Successfully! Đã nạp {len(food101_list)} món vào collection 'food101'.")

print("\n Toàn bộ dữ liệu đã được làm phẳng và đẩy lên MongoDB Atlas thành công!")