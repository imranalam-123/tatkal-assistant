from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from backend.database import SessionLocal

from backend.models.ticket import Ticket
from backend.models.booking import Booking
from backend.models.passenger import Passenger

from backend.dependencies.auth_dependency import get_current_user

from reportlab.pdfgen import canvas

import random


router = APIRouter(
    prefix="/ticket",
    tags=["Ticket"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================
# GENERATE TICKET
# ==========================
@router.post("/generate/{booking_id}")
def generate_ticket(
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

    existing_ticket = db.query(
        Ticket
    ).filter(
        Ticket.booking_id == booking_id
    ).first()

    if existing_ticket:
        return {
            "message": "Ticket already generated",
            "ticket_id": existing_ticket.id,
            "ticket_number": existing_ticket.ticket_number
        }

    ticket = Ticket(
        ticket_number=f"TKT{random.randint(100000,999999)}",
        booking_id=booking.id,
        user_id=current_user.id,
        pnr=booking.pnr
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket generated successfully",
        "ticket_id": ticket.id,
        "ticket_number": ticket.ticket_number
    }


# ==========================
# GET ALL TICKETS
# ==========================
@router.get("/all")
def get_my_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    tickets = db.query(
        Ticket
    ).filter(
        Ticket.user_id == current_user.id
    ).all()

    return tickets


# ==========================
# GET TICKET DETAILS
# ==========================
@router.get("/{ticket_id}")
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    ticket = db.query(
        Ticket
    ).filter(
        Ticket.id == ticket_id,
        Ticket.user_id == current_user.id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    booking = db.query(
        Booking
    ).filter(
        Booking.id == ticket.booking_id
    ).first()

    passenger = db.query(
        Passenger
    ).filter(
        Passenger.id == booking.passenger_id
    ).first()

    return {
        "ticket_id": ticket.id,
        "ticket_number": ticket.ticket_number,
        "pnr": ticket.pnr,

        "train_no": booking.train_no,
        "journey_date": booking.journey_date,

        "status": booking.status,
        "rac_number": booking.rac_number,
        "wl_number": booking.wl_number,

        "passenger": {
            "id": passenger.id,
            "name": passenger.name,
            "age": passenger.age,
            "gender": passenger.gender,
            "berth_preference": passenger.berth_preference
        }
    }


# ==========================
# DOWNLOAD PDF TICKET
# ==========================
@router.get("/download/{ticket_id}")
def download_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    ticket = db.query(
        Ticket
    ).filter(
        Ticket.id == ticket_id,
        Ticket.user_id == current_user.id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    booking = db.query(
        Booking
    ).filter(
        Booking.id == ticket.booking_id
    ).first()

    passenger = db.query(
        Passenger
    ).filter(
        Passenger.id == booking.passenger_id
    ).first()

    pdf_file = f"ticket_{ticket.id}.pdf"

    c = canvas.Canvas(pdf_file)

    c.setFont(
        "Helvetica-Bold",
        18
    )

    c.drawString(
        170,
        800,
        "Tatkal Assistant Ticket"
    )

    c.setFont(
        "Helvetica",
        12
    )

    c.drawString(
        100,
        740,
        f"Ticket Number: {ticket.ticket_number}"
    )

    c.drawString(
        100,
        710,
        f"PNR: {ticket.pnr}"
    )

    c.drawString(
        100,
        680,
        f"Booking ID: {booking.id}"
    )

    c.drawString(
        100,
        650,
        f"Train Number: {booking.train_no}"
    )

    c.drawString(
        100,
        620,
        f"Passenger Name: {passenger.name}"
    )

    c.drawString(
        100,
        590,
        f"Age: {passenger.age}"
    )

    c.drawString(
        100,
        560,
        f"Gender: {passenger.gender}"
    )

    c.drawString(
        100,
        530,
        f"Berth Preference: {passenger.berth_preference}"
    )

    c.drawString(
        100,
        500,
        f"Journey Date: {booking.journey_date}"
    )

    c.drawString(
        100,
        470,
        f"Status: {booking.status}"
    )

    if booking.rac_number:
        c.drawString(
            100,
            440,
            f"RAC Number: {booking.rac_number}"
        )

    if booking.wl_number:
        c.drawString(
            100,
            410,
            f"WL Number: {booking.wl_number}"
        )

    c.save()

    return FileResponse(
        path=pdf_file,
        filename=pdf_file,
        media_type="application/pdf"
    )