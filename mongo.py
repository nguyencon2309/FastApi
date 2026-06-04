import os
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

#
# 1. Cấu hình Kết nối MongoDB
MONGO_URI = os.getenv("MONGO_URL")
DB_NAME = "smart_tray"
COLLECTION_NAME = "food102"

# 2. Đường dẫn tới file Excel của bạn
# Giả sử file Excel tên là "danh_sach_mon_an.xlsx" nằm cùng thư mục với file code này
EXCEL_FILE_PATH = r'C:\Users\Admin\Documents\Book2_food_db.xlsx'

def import_excel_to_mongodb():
    # Kiểm tra xem file Excel có tồn tại không
    if not os.path.exists(EXCEL_FILE_PATH):
        print(f"❌ Không tìm thấy file Excel tại đường dẫn: {EXCEL_FILE_PATH}")
        return

    print("📖 Đang đọc dữ liệu từ file Excel...")
    # Đọc file Excel bằng cấu trúc DataFrame của Pandas
    df = pd.read_excel(EXCEL_FILE_PATH,sheet_name='Sheet1')

    # In thử các cột hiện có trong file để kiểm tra
    print(f"📋 Các cột tìm thấy trong file: {list(df.columns)}")

    # Kết nối tới MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    documents_to_insert = []

    print("⏳ Đang chuẩn hóa dữ liệu sang định dạng MongoDB...")
    # Lặp qua từng dòng (row) trong file Excel
    for index, row in df.iterrows():
        try:
            # Lấy dữ liệu và xử lý giá trị NaN (nếu có ô trống trong Excel)
            className = str(row['className']).strip() if pd.notna(row['className']) else ""
            nameViet = str(row['name']).strip() if pd.notna(row['name']) else ""
            
            category = str(row['category']).strip() if pd.notna(row['category']) else ""
            description = str(row['description']).strip() if pd.notna(row['description']) else ""
            price = int(str(row['price']).strip()) 
            calories = int(str(row['calories']).strip())
            image = str(row['image']).strip() if pd.notna(row['image']) else ""
            # Xử lý cắt chuỗi ngăn cách bởi dấu gạch đứng '|' thành list
            ingredients_raw = str(row['ingredients']) if pd.notna(row['ingredients']) else ""
            ingredients_list = [item.strip() for item in ingredients_raw.split('|') if item.strip()]

            recipe_raw = str(row['recipe']) if pd.notna(row['recipe']) else ""
            recipe_list = [item.strip() for item in recipe_raw.split('|') if item.strip()]

            tips_raw = str(row['tips']).strip() if pd.notna(row['tips']) else ""
            tips_list = [item.strip() for item in tips_raw.split('|') if item.strip()]  

            # Bỏ qua nếu dòng đó trống tên món ăn
            if not nameViet or nameViet == "nan":
                continue

            # Tạo cấu trúc Document chuẩn khớp với Schema FastAPI
            # MongoDB sẽ tự hiểu khóa chính là '_id' kiểu ObjectId
            dish_document = {
                "_id": ObjectId(), # Tự sinh một ObjectId mới cho mỗi món ăn
                "className": className,
                "nameViet": nameViet,
                "image":image,
                "category": category,
                "description": description,
                "price": price,
                "calories": calories,
                "ingredients": ingredients_list,
                "recipe": recipe_list,
                "tips": tips_list
            }

            documents_to_insert.append(dish_document)

        except KeyError as e:
            print(f"❌ Lỗi: File Excel thiếu cột bắt buộc: {e}")
            print("Vui lòng đảm bảo file có đủ các cột: 'Tên món ăn', 'ingredients', 'recipe', 'tips'")
            return
        except Exception as e:
            print(f"⚠️ Lỗi xử lý ở dòng {index + 2}: {e}")

    # Tiến hành insert vào Database
    if documents_to_insert:
        print(f"🚀 Đang chèn {len(documents_to_insert)} món ăn vào MongoDB...")
        # Xóa dữ liệu cũ nếu muốn (Tùy chọn: bỏ comment dòng dưới nếu muốn làm sạch data cũ trước khi nạp)
        # collection.delete_many({}) 
        
        # Chèn toàn bộ mảng data vào Mongo
        result = collection.insert_many(documents_to_insert)
        print(f"🎉 Thành công! Đã import thành công {len(result.inserted_ids)} món ăn vào bộ sưu tập '{COLLECTION_NAME}'.")
    else:
        print("🤷 Không có dữ liệu hợp lệ nào được tìm thấy để import.")

    # Đóng kết nối
    client.close()

if __name__ == "__main__":
    import_excel_to_mongodb()