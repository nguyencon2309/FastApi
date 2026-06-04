from app.core.database import db
from app.schemas.food_schemas import Food
from fastapi import FastAPI, HTTPException, status
from bson import ObjectId
from app.utils.helper import pydantic_mongo_helper  
food_col = db["food102"]




def get_foods():
    
    cursor = food_col.find({}, {"imageUrl":0,"vietnamese_name":0,"firebase_key":0,"className":0,"description":0})
    raw_foods = cursor.to_list()
    cleaned_food = [pydantic_mongo_helper(food) for food in raw_foods]
    
    return cleaned_food




def get_food_by_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    rs= food_col.find_one({"_id": ObjectId(id)}, {"imageUrl":0,"vietnamese_name":0,"firebase_key":0})
    if rs is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return pydantic_mongo_helper(rs)


def update_food(id: str, data: Food):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    update_data = data.dict(exclude_unset=True)
    update_data.pop("_id", None)
    update_data.pop("image",None)
    update_data.pop("className",None)
    update_data.pop("nameViet",None)
    update_data.pop("vietnamese_name",None)
    food_col.update_one({"_id": ObjectId(id)}, {"$set":update_data})
    return {"message": "updated"}


