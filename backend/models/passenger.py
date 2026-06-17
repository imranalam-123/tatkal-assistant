from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database import Base


class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    age = Column(Integer, nullable=False)

    gender = Column(String, nullable=False)

    berth_preference = Column(String)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )