from fastapi import APIRouter, Form, UploadFile,File, Depends
from app.middleware.auth_middleware import check_token_middleware,check_admin_middleware

from app.services import history_service


router = APIRouter()

@router.post("/")
async def add(file:UploadFile = File(...), data: str=Form(...),current_user: dict = Depends(check_token_middleware)):
    user_id = str(current_user.get("_id"))
    return await history_service.add_history(file, data, user_id)
@router.get("/id")
def get(id: str,current_user: dict = Depends(check_token_middleware)):
    user_id = str(current_user.get("_id"))
    return history_service.get_history(id, user_id)
@router.get("/",dependencies=[Depends(check_token_middleware)])
def get(current_user: dict = Depends(check_token_middleware)):
    user_id = str(current_user.get("_id"))
    return history_service.get_all_history(user_id)

@router.delete("/all",dependencies=[Depends(check_admin_middleware)])
def delete_all():
    return history_service.delete_all_history()


@router.delete("/{id}",dependencies=[Depends(check_token_middleware)])
def delete(id: str, current_user: dict = Depends(check_token_middleware)):
    user_id = str(current_user.get("_id"))
    return history_service.delete_history(id,user_id)
