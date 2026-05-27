from fastapi import APIRouter, Form, UploadFile,File

from app.services import history_service


router = APIRouter()

@router.post("/")
async def add(file:UploadFile = File(...), data: str=Form(...)):
    return await history_service.add_history(file, data)
@router.get("/id")
def get(id: str):
    return history_service.get_history(id)
@router.get("/")
def get():
    return history_service.get_all_history()

@router.delete("/{id}")
def delete(id: str):
    return history_service.delete_history(id)