from sqlalchemy import Column, Integer, String

from backend.database import Base


class Availability(Base):
    __tablename__ = "availability"

    id = Column(Integer, primary_key=True, index=True)

    train_no = Column(String, index=True)

    journey_date = Column(String)

    available_seats = Column(Integer)

    # NEW
    rac_count = Column(Integer, default=0)

    waiting_list = Column(Integer, default=0)