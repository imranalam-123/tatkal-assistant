from pydantic import BaseModel


class AvailabilityCreate(BaseModel):
    train_no: str
    journey_date: str
    available_seats: int
    waiting_list: int = 0