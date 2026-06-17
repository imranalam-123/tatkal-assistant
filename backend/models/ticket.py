from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime

from backend.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id")
    )

    pnr = Column(
        String,
        unique=True,
        nullable=False
    )

    ticket_number = Column(
        String,
        unique=True,
        nullable=False
    )

    generated_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )