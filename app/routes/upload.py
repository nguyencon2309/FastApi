from fastapi import UploadFile, File
from app.services import upload_service



async def upload(file: UploadFile = File(...)):
    return upload_service.upload_image(file.file)


def delete(public_id: str):
    return upload_service.delete_image(public_id)