from sqlalchemy import Column, Integer, String, Float, ForeignKey
from backend.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(Integer, ForeignKey("bookings.id"))

    amount = Column(Float)

    payment_method = Column(String)

    transaction_id = Column(String, unique=True)

    status = Column(String, default="SUCCESS")

    user_id = Column(Integer, ForeignKey("users.id"))