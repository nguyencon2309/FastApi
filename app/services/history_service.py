from bson import ObjectId

from app.core.database import db

from app.routes.upload import upload,delete
from fastapi import  Form, UploadFile,File
import json

history_col = db["history"]

async def add_history(file: UploadFile = File(...),
    data: str = Form(...)):
    history_data = json.loads(data)
    upload_result = await upload(file)
    history_data["imagePredict"] = upload_result["url"] 
    history_data["image_public_id"] = upload_result["public_id"]    

    if "_id" not in history_data:
        history_data["_id"] = ObjectId()
    
    history_data["id"] = str(history_data["_id"])
    result = history_col.insert_one(history_data)
    return {
       "status": "success",
        
        "imageUrl": upload_result["url"]
    }
    
def get_all_history():
    return list(history_col.find({}, {"_id": 0}))

def get_history(id: str):
 
    return   list(
            history_col.find(
                {"id": id},
                {"_id": 0}
            ).sort("timestamp",-1))
def get_history_by_id(history_id: str):
    return history_col.find_one({"_id": history_id}, {"_id": 0})

def delete_history(history_id: str):
    history = get_history_by_id(history_id)
    if history and history.get("image_public_id"):
        delete(history["image_public_id"])
    history_col.delete_one({"_id": history_id})
    

    return {"message": "deleted"}



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