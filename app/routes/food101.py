from fastapi import APIRouter
from app.schemas.food_schemas import Food
from app.services import food101_service

router = APIRouter()


@router.get("/")
def get_all():
    return food101_service.get_foods()

@router.get("/{id}")
def get_one(id: str):
    return food101_service.get_food_by_id(id)

@router.put("/{id}")
def update(id: str, food: Food):
    return food101_service.update_food(id, food.dict())
