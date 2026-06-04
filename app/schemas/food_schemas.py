from bson import ObjectId
from typing import Any
from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import core_schema

class Food(BaseModel):
    image: str | None = None
    className: str
    description: str
    nameViet: str
    price: int = 0
    id: str
    category:str =""
    calories: int = 0
    ingredients: list[str] = Field(default_factory=list)
    recipe: list[str] = Field(default_factory=list)
    tips: list[str] = Field(default_factory=list)

    class Config:
        from_attributes = True



