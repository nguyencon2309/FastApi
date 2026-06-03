from fastapi import APIRouter,Depends
from app.middleware.auth_middleware import check_admin_middleware, check_token_middleware
from app.schemas.food_schemas import Food
from app.services import food_service

router = APIRouter()


@router.get("/",dependencies=[Depends(check_token_middleware)])
def get_all():
    return food_service.get_foods()

@router.get("/{id}",dependencies=[Depends(check_token_middleware)])
def get_one(id: str):
    return food_service.get_food_by_id(id)

@router.put("/{id}",dependencies=[Depends(check_admin_middleware)])
def update(id: str, food:Food):
    return food_service.update_food(id, food)
