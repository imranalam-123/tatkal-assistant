from pydantic import BaseModel


class PassengerCreate(BaseModel):
    name: str
    age: int
    gender: str
    berth_preference: str