from pydantic import BaseModel,Field
from bson import ObjectId




class user(BaseModel):
    username:str
    password:str
    email:str
    role:str="user"
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=6)
    password: str = Field(..., min_length=6)
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  
class UserLoginSchema(BaseModel):
    email: str
    password: str  
