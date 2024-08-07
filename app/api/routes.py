from fastapi import APIRouter
from app.api.endpoints import receipts

# Main API router
router = APIRouter()

# Include the receipts router
router.include_router(receipts.router, prefix="/receipts", tags=["receipts"])