from fastapi import FastAPI
from app.routes import food, history, food101

app = FastAPI(title="Food Backend API")

app.include_router(food.router, prefix="/foods", tags=["Foods"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(food101.router, prefix="/food101", tags=["Food101"])

#uvicorn app.main:app --reload --port 8000