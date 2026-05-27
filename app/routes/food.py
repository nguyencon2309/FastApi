from fastapi import APIRouter
from app.schemas.food_schemas import Food
from app.services import food_service

router = APIRouter()


@router.get("/")
def get_all():
    return food_service.get_foods()

@router.get("/{id}")
def get_one(id: str):
    return food_service.get_food_by_id(id)

@router.put("/{id}")
def update(id: str, food: Food):
    return food_service.update_food(id, food.dict())
