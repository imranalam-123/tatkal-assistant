from sqlalchemy import Column, Integer, String, ForeignKey

from backend.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    pnr = Column(
        String,
        unique=True,
        index=True
    )

    train_no = Column(String)

    journey_date = Column(String)

    status = Column(
        String,
        default="CONFIRMED"
    )

    # RAC NUMBER
    rac_number = Column(
        Integer,
        nullable=True
    )

    # WAITING LIST NUMBER
    wl_number = Column(
        Integer,
        nullable=True
    )

    # COACH DETAILS
    coach = Column(
        String,
        nullable=True
    )

    seat_no = Column(
        Integer,
        nullable=True
    )

    berth = Column(
        String,
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    passenger_id = Column(
        Integer,
        ForeignKey("passengers.id")
    )