from typing import List

from bson import ObjectId
from pydantic import BaseModel

from app.schemas.invoice_schemas import Invoice

class History(BaseModel):
    _id: ObjectId | None = None
    imagePredict:str | None = None
    image_public_id:str | None = None
    id:str | None = None
    timestamp:int
    listInvoice:List[Invoice]=[]
    user_id:str | None = None
    sumPrice:int | None = None
    quanlityFood:int | None = None
