from fastapi import FastAPI
from app.routes import food, history, food101, user
import os
import sys
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Food Backend API")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get("/")
def read_root():
    return {"message": "Backend SmartTray"}
app.include_router(food.router, prefix="/foods", tags=["Foods"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(food101.router, prefix="/food101", tags=["Food101"])
app.include_router(user.router, prefix="/auth", tags=["Users"])

# #uvicorn app.main:app --reload --port 8000
# from app.main import app

