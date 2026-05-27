from fastapi import FastAPI
from app.routes import food, history, food101
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="Food Backend API")
@app.get("/")
def read_root():
    return {"message": "Backend SmartTray"}
app.include_router(food.router, prefix="/foods", tags=["Foods"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(food101.router, prefix="/food101", tags=["Food101"])

#uvicorn app.main:app --reload --port 8000