from bson import ObjectId

from app.core.database import db

from app.routes.upload import upload,delete
from fastapi import  Form, UploadFile,File
import json

history_col = db["history"]

async def add_history(file: UploadFile = File(...),
    data: str = Form(...), user_id: str = None):
    history_data = json.loads(data)
    upload_result = await upload(file)
    history_data["imagePredict"] = upload_result["url"] 
    history_data["image_public_id"] = upload_result["public_id"]    
    history_data["user_id"] = user_id
    history_data["quanlityFood"] = len(history_data.get("listInvoice", []))
    history_data["sumPrice"] = sum(invoice.get("price", 0) for invoice in history_data.get("listInvoice", []))

    if "_id" not in history_data:
        history_data["_id"] = ObjectId()
    
    history_data["id"] = str(history_data["_id"])
    result = history_col.insert_one(history_data)
    return {
       "status": "success",
        
        "imageUrl": upload_result["url"]
    }
    
def get_all_history(user_id: str):
    return list(history_col.find({"user_id": user_id}, {"_id": 0,"listInvoice": 0,"user_id": 0,"image_public_id": 0}).sort("timestamp",-1))

# def get_history(id: str,user_id: str):
 
#     return   list(
#             history_col.find(
#                 {"id": id, "user_id": user_id},
#                 {"_id": 0,"listInvoice": 0,"user_id": 0,"image_public_id": 0}
#             ))
def get_history_by_id(history_id: str, user_id: str):
    return history_col.find_one({"id": history_id, "user_id": user_id}, {"_id": 0,"user_id": 0,"image_public_id": 0})

def delete_history(history_id: str, user_id: str):
    history = get_history_by_id(history_id, user_id)
    if history and history.get("image_public_id"):
        delete(history["image_public_id"])
    history_col.delete_one({"id": history_id, "user_id": user_id})
    

    return {"message": "deleted"}
def delete_all_history():
    all_history = list(history_col.find({}, {"_id": 0}))
    for history in all_history:
        if history.get("image_public_id"):
            delete(history["image_public_id"])
    history_col.delete_many({})
    return {"message": "deleted all"}


"""
xử lí truy vấn mongodb
pipeline = [
    {"$match": {"id": id}},            # 1. Tìm kiếm (Filter)
    {"$sort": {"timestamp": -1}},      # 2. Sắp xếp (Sort)
    {"$project": {"_id": 0}},          # 3. Ẩn/Hiện field (Projection)
    # {"$limit": 10}                   # 4. Giới hạn nếu cần (Ví dụ lấy 10 lịch sử gần nhất)
]

history_list = list(history_col.aggregate(pipeline))
"""