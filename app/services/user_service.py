from bson import ObjectId

from app.core.database import db

from fastapi import  Form, UploadFile,File
import json
from fastapi import APIRouter, Depends
from app.schemas.user_schemas import UserCreate, UserLoginSchema
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.security import get_password_hash, verify_password, create_access_token
user_col = db["user"]

def register_user(user_in: UserCreate):
    # Bước A: Kiểm tra xem email đã tồn tại trong Collection chưa
    existing_user =user_col.find_one({"email": user_in.email})
    if existing_user:
        return {"error": "Email đã tồn tại. Vui lòng sử dụng email khác."}
        
    
    hashed_password = get_password_hash(user_in.password)
    user_data = {
        "username": user_in.username,
        "email": user_in.email,
        "password": hashed_password,
        "role": "user"
    }
    result = user_col.insert_one(user_data)
    
    created_user =  user_col.find_one({"_id": result.inserted_id},{"_id": 0, "password": 0})  
    
    
    return created_user



def login_user(form_data: UserLoginSchema):
    user = user_col.find_one({"email": form_data.email})
    if not user or not verify_password(form_data.password, user["password"]):
        return {"error": "Email hoặc mật khẩu không đúng!"}
        
    access_token = create_access_token(data={"sub": str(user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}