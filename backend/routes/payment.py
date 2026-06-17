from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random

from backend.database import get_db
from backend.dependencies.auth_dependency import get_current_user

from backend.models.user import User
from backend.models.booking import Booking
from backend.models.payment import Payment

from backend.schemas.payment import PaymentCreate

router = APIRouter(
    prefix="/payment",
    tags=["Payment"]
)


# ==========================
# Make Payment
# ==========================
@router.post("/pay")
def make_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    booking = (
        db.query(Booking)
        .filter(
            Booking.id == payment.booking_id,
            Booking.user_id == current_user.id
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.status == "CANCELLED":
        raise HTTPException(
            status_code=400,
            detail="Cannot pay for cancelled booking"
        )

    transaction_id = f"TXN{random.randint(100000,999999)}"

    new_payment = Payment(
        booking_id=payment.booking_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        transaction_id=transaction_id,
        status="SUCCESS",
        user_id=current_user.id
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return {
        "message": "Payment successful",
        "payment_id": new_payment.id,
        "transaction_id": transaction_id,
        "amount": payment.amount,
        "status": "SUCCESS"
    }


# ==========================
# Get My Payments
# ==========================
@router.get("/all")
def get_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    payments = (
        db.query(Payment)
        .filter(Payment.user_id == current_user.id)
        .all()
    )

    return payments


# ==========================
# Get Payment By ID
# ==========================
@router.get("/{payment_id}")
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    payment = (
        db.query(Payment)
        .filter(
            Payment.id == payment_id,
            Payment.user_id == current_user.id
        )
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment