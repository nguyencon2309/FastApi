from app.core.database import db

food_col = db["food101"]




def get_foods():
    return list(food_col.find({}, {"_id": 0}))


def get_food_by_id(id: str):
    return food_col.find_one({"id": id}, {"_id": 0})


def update_food(id: str, data: dict):
    food_col.update_one({"id": id}, {"$set": data})
    return {"message": "updated"}


