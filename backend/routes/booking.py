from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db

from backend.schemas.booking import BookingCreate

from backend.models.booking import Booking
from backend.models.passenger import Passenger
from backend.models.availability import Availability

from backend.dependencies.auth_dependency import (
    get_current_user
)

import random


router = APIRouter(
    prefix="/booking",
    tags=["Booking"]
)

MAX_RAC = 2


@router.post("/create")
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    passenger = db.query(
        Passenger
    ).filter(
        Passenger.id == booking.passenger_id,
        Passenger.user_id == current_user.id
    ).first()

    if not passenger:
        raise HTTPException(
            status_code=404,
            detail="Passenger not found"
        )

    availability = db.query(
        Availability
    ).filter(
        Availability.train_no == booking.train_no,
        Availability.journey_date == str(booking.journey_date)
    ).first()

    if not availability:
        raise HTTPException(
            status_code=404,
            detail="Availability not found"
        )

    pnr = str(
        random.randint(
            1000000000,
            9999999999
        )
    )

    booking_status = "CONFIRMED"

    rac_number = None
    wl_number = None

    coach = None
    seat_no = None
    berth = None

    # ==========================
    # CONFIRMED
    # ==========================
    if availability.available_seats > 0:

        availability.available_seats -= 1

        coach = f"S{random.randint(1,3)}"
        seat_no = random.randint(1,72)
        berth = passenger.berth_preference

    # ==========================
    # RAC
    # ==========================
    elif availability.rac_count < MAX_RAC:

        booking_status = "RAC"

        availability.rac_count += 1

        rac_number = availability.rac_count

    # ==========================
    # WAITING
    # ==========================
    else:

        booking_status = "WAITING"

        availability.waiting_list += 1

        wl_number = availability.waiting_list

    new_booking = Booking(
        pnr=pnr,
        train_no=booking.train_no,
        journey_date=booking.journey_date,

        status=booking_status,

        rac_number=rac_number,
        wl_number=wl_number,

        coach=coach,
        seat_no=seat_no,
        berth=berth,

        user_id=current_user.id,
        passenger_id=booking.passenger_id
    )

    db.add(new_booking)

    db.commit()

    db.refresh(new_booking)

    return {
        "booking_id": new_booking.id,
        "pnr": new_booking.pnr,

        "status": new_booking.status,

        "coach": new_booking.coach,
        "seat_no": new_booking.seat_no,
        "berth": new_booking.berth,

        "rac_number": new_booking.rac_number,
        "wl_number": new_booking.wl_number,

        "available_seats": availability.available_seats,
        "rac_count": availability.rac_count,
        "waiting_list": availability.waiting_list
    }


@router.get("/all")
def get_bookings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(
        Booking
    ).filter(
        Booking.user_id == current_user.id
    ).all()


@router.get("/{booking_id}")
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    booking = db.query(
        Booking
    ).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return booking


@router.delete("/cancel/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    booking = db.query(
        Booking
    ).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.status == "CANCELLED":
        raise HTTPException(
            status_code=400,
            detail="Booking already cancelled"
        )

    availability = db.query(
        Availability
    ).filter(
        Availability.train_no == booking.train_no,
        Availability.journey_date == str(booking.journey_date)
    ).first()

    # =====================================
    # CANCEL CONFIRMED BOOKING
    # =====================================
    if booking.status == "CONFIRMED":

        rac_booking = db.query(
            Booking
        ).filter(
            Booking.train_no == booking.train_no,
            Booking.journey_date == str(booking.journey_date),
            Booking.status == "RAC"
        ).order_by(
            Booking.rac_number.asc()
        ).first()

        if rac_booking:

            rac_booking.status = "CONFIRMED"
            rac_booking.rac_number = None

            passenger = db.query(
                Passenger
            ).filter(
                Passenger.id == rac_booking.passenger_id
            ).first()

            rac_booking.coach = f"S{random.randint(1,3)}"
            rac_booking.seat_no = random.randint(1,72)
            rac_booking.berth = passenger.berth_preference

            availability.rac_count -= 1

            db.flush()

            remaining_rac = db.query(
                Booking
            ).filter(
                Booking.train_no == booking.train_no,
                Booking.journey_date == str(booking.journey_date),
                Booking.status == "RAC"
            ).order_by(
                Booking.rac_number.asc()
            ).all()

            counter = 1

            for item in remaining_rac:
                item.rac_number = counter
                counter += 1

            wl_booking = db.query(
                Booking
            ).filter(
                Booking.train_no == booking.train_no,
                Booking.journey_date == str(booking.journey_date),
                Booking.status == "WAITING"
            ).order_by(
                Booking.wl_number.asc()
            ).first()

            if wl_booking:

                wl_booking.status = "RAC"
                wl_booking.rac_number = availability.rac_count + 1
                wl_booking.wl_number = None

                availability.rac_count += 1
                availability.waiting_list -= 1

                db.flush()

                remaining_wl = db.query(
                    Booking
                ).filter(
                    Booking.train_no == booking.train_no,
                    Booking.journey_date == str(booking.journey_date),
                    Booking.status == "WAITING"
                ).order_by(
                    Booking.wl_number.asc()
                ).all()

                counter = 1

                for item in remaining_wl:
                    item.wl_number = counter
                    counter += 1

        else:

            availability.available_seats += 1

    # =====================================
    # CANCEL RAC BOOKING
    # =====================================
    elif booking.status == "RAC":

        availability.rac_count -= 1

        wl_booking = db.query(
            Booking
        ).filter(
            Booking.train_no == booking.train_no,
            Booking.journey_date == str(booking.journey_date),
            Booking.status == "WAITING"
        ).order_by(
            Booking.wl_number.asc()
        ).first()

        if wl_booking:

            wl_booking.status = "RAC"
            wl_booking.rac_number = availability.rac_count + 1
            wl_booking.wl_number = None

            availability.rac_count += 1
            availability.waiting_list -= 1

        remaining_rac = db.query(
            Booking
        ).filter(
            Booking.train_no == booking.train_no,
            Booking.journey_date == str(booking.journey_date),
            Booking.status == "RAC",
            Booking.id != booking.id
        ).order_by(
            Booking.rac_number.asc()
        ).all()

        counter = 1

        for item in remaining_rac:
            item.rac_number = counter
            counter += 1

    # =====================================
    # CANCEL WAITING BOOKING
    # =====================================
    elif booking.status == "WAITING":

        availability.waiting_list -= 1

        remaining_wl = db.query(
            Booking
        ).filter(
            Booking.train_no == booking.train_no,
            Booking.journey_date == str(booking.journey_date),
            Booking.status == "WAITING",
            Booking.id != booking.id
        ).order_by(
            Booking.wl_number.asc()
        ).all()

        counter = 1

        for item in remaining_wl:
            item.wl_number = counter
            counter += 1

    booking.status = "CANCELLED"

    db.commit()

    return {
        "message": "Booking cancelled successfully",
        "booking_id": booking.id,
        "status": booking.status,
        "available_seats": availability.available_seats,
        "rac_count": availability.rac_count,
        "waiting_list": availability.waiting_list
    }