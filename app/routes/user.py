from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.food_schemas import Food
from app.schemas.user_schemas import UserCreate, UserLoginSchema
from app.services import food_service
from app.services.user_service import register_user,login_user

router = APIRouter()


@router.post("/register")
def register(user_in: UserCreate):
    return register_user(user_in)

@router.post("/login")
def login(form_data: UserLoginSchema):
    return login_user(form_data)
