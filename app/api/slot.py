from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.slot import SlotResponse
from app.services.slot_service import get_available_slots

router = APIRouter(
    prefix="/slots",
    tags=["Slots"],
)

@router.get(
    "/",
    response_model=List[SlotResponse],
)
def list_available_slots(
    db: Session = Depends(get_db),
):
    return get_available_slots(db)