from sqlalchemy.orm import Session

from backend.models.passenger import Passenger


def create_passenger(
    db: Session,
    passenger_data,
    user_id: int
):
    passenger = Passenger(
        name=passenger_data.name,
        age=passenger_data.age,
        gender=passenger_data.gender,
        berth_preference=passenger_data.berth_preference,
        user_id=user_id
    )

    db.add(passenger)
    db.commit()
    db.refresh(passenger)

    return passenger


def get_all_passengers(
    db: Session,
    user_id: int
):
    return db.query(Passenger).filter(
        Passenger.user_id == user_id
    ).all()