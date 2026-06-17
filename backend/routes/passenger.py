from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db

from backend.schemas.passenger import (
    PassengerCreate
)

from backend.services.passenger_service import (
    create_passenger,
    get_all_passengers
)

from backend.dependencies.auth_dependency import (
    get_current_user
)

router = APIRouter(
    prefix="/passenger",
    tags=["Passenger"]
)


@router.post("/add")
def add_passenger(
    passenger: PassengerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_passenger = create_passenger(
        db,
        passenger,
        current_user.id
    )

    return {
        "message": "Passenger added successfully",
        "passenger_id": new_passenger.id
    }


@router.get("/all")
def get_passengers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    passengers = get_all_passengers(
        db,
        current_user.id
    )

    return passengers