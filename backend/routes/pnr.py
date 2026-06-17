from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.booking import Booking

router = APIRouter(
    prefix="/pnr",
    tags=["PNR Status"]
)


@router.get("/{pnr}")
def check_pnr(
    pnr: str,
    db: Session = Depends(get_db)
):
    booking = db.query(
        Booking
    ).filter(
        Booking.pnr == pnr
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="PNR not found"
        )

    return {
        "pnr": booking.pnr,
        "train_no": booking.train_no,
        "journey_date": booking.journey_date,
        "status": booking.status,
        "rac_number": booking.rac_number,
        "wl_number": booking.wl_number
    }