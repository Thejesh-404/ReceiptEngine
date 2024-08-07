from pydantic import BaseModel, Field
from typing import List

class Item(BaseModel):
    shortDescription: str = Field(..., pattern=r"^[\w\s\-]+$")
    price: str = Field(..., pattern=r"^\d+\.\d{2}$")

class Receipt(BaseModel):
    retailer: str = Field(..., pattern=r"^[\w\s\-&]+$")
    purchaseDate: str = Field(..., format="date")
    purchaseTime: str = Field(..., format="time")
    items: list[Item] = Field(..., min_length=1)
    total: str = Field(..., pattern=r"^\d+\.\d{2}$")

class ReceiptResponse(BaseModel):
    id: str = Field(..., pattern=r"^\S+$")

class PointsResponse(BaseModel):
    points: int
