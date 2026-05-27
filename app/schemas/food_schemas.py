
from pydantic import BaseModel
from bson import ObjectId

class Food(BaseModel):
    name: str
    calories: float
    image: str | None = None
    _id: ObjectId | None = None
    classname: str
    description: str
    nameViet: str
    price: int
    id:str



