
from pydantic import BaseModel
from bson import ObjectId

class Food(BaseModel):
    image: str | None = None
    className: str
    description: str
    nameViet: str
    price: int
    id:str


