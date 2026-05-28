from app.core.database import db
from app.schemas.food_schemas import Food

food_col = db["food101"]



def get_foods():
    return list(food_col.find({}, {"_id": 0,"imageUrl":0,"vietnamese_name":0,"firebase_key":0}))


def get_food_by_id(id: str):
    return food_col.find_one({"id": id}, {"_id": 0})


def update_food(id: str, data: Food):
    update_data = data.dict(exclude_unset=True)
    update_data.pop("_id", None)
    update_data.pop("image",None)
    update_data.pop("classname",None)
    update_data.pop("nameViet",None)
    update_data.pop("vietnamese_name",None)
    food_col.update_one({"id": id}, {"$set":update_data})
    return {"message": "updated"}

