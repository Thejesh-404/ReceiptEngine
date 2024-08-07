from fastapi import APIRouter, HTTPException, status
from app.schemas.receipt import Receipt, ReceiptResponse, PointsResponse
from app.services.receipt_service import process_receipt, get_receipt_points
from pydantic import ValidationError
from datetime import datetime
from uuid import uuid4

router = APIRouter()

@router.post("/process", response_model=ReceiptResponse, status_code=status.HTTP_201_CREATED)
async def process_receipt_endpoint(receipt: Receipt):   
    # Validate date and time format
    try:
        datetime.strptime(receipt.purchaseDate, "%Y-%m-%d")
        datetime.strptime(receipt.purchaseTime, "%H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date or time format")
    
    # Validate total matches sum of item prices
    total = sum(float(item.price) for item in receipt.items)
    if abs(float(receipt.total) - total) > 0.01:
        raise HTTPException(status_code=400, detail="Total does not match sum of item prices")
    
    receipt_id = str(uuid4())
    process_receipt(receipt, receipt_id)
    return {"id": receipt_id}


@router.get("/{id}/points", response_model=PointsResponse, status_code=status.HTTP_200_OK)
async def get_points_endpoint(id: str):
    points = get_receipt_points(id)
    if points is None:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return {"points" : points}