from pydantic import BaseModel

class Invoice(BaseModel):
    name: str
    quantity: int
    price: int
    idFood: str