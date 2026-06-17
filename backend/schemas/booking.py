from pydantic import BaseModel


class BookingCreate(BaseModel):
    passenger_id: int
    train_no: str
    journey_date: str