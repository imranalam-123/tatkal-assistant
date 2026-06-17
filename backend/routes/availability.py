from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models.availability import Availability
from backend.schemas.availability import AvailabilityCreate

router = APIRouter(
    prefix="/availability",
    tags=["Availability"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_availability(
    availability: AvailabilityCreate,
    db: Session = Depends(get_db)
):
    new_record = Availability(
        train_no=availability.train_no,
        journey_date=str(availability.journey_date),
        available_seats=availability.available_seats,
        waiting_list=availability.waiting_list
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {
        "message": "Availability added",
        "id": new_record.id
    }


@router.get("/{train_no}/{journey_date}")
def check_availability(
    train_no: str,
    journey_date: str,
    db: Session = Depends(get_db)
):
    record = db.query(Availability).filter(
        Availability.train_no == train_no,
        Availability.journey_date == journey_date
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Availability not found"
        )

    return {
        "train_no": record.train_no,
        "journey_date": record.journey_date,
        "available_seats": record.available_seats,
        "waiting_list": record.waiting_list
    }