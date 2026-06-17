from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models.booking import Booking
from backend.models.ticket import Ticket
from backend.models.payment import Payment

from backend.dependencies.auth_dependency import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats")
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    total_bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).count()

    total_tickets = db.query(Ticket).filter(
        Ticket.user_id == current_user.id
    ).count()

    total_payments = db.query(Payment).filter(
        Payment.user_id == current_user.id
    ).count()

    return {
        "total_bookings": total_bookings,
        "total_tickets": total_tickets,
        "total_payments": total_payments
    }