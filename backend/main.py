from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine

# IMPORT MODELS
from backend.models.user import User
from backend.models.booking import Booking
from backend.models.ticket import Ticket
from backend.models.payment import Payment

# IMPORT ROUTES
from backend.routes import auth
from backend.routes import user
from backend.routes import train
from backend.routes import passenger
from backend.routes import booking
from backend.routes import payment
from backend.routes import ticket
from backend.routes import availability
from backend.routes import pnr
from backend.routes import dashboard

# =========================
# Create Database Tables
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# FastAPI App
# =========================
app = FastAPI(
    title="Tatkal Assistant API",
    version="1.0.0",
    description="Railway Tatkal Booking Assistant Backend"
)

# =========================
# CORS Configuration
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Local Frontend URLs
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",

        # Render Frontend URL
        "https://tatkal-assistant-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Routes
# =========================

# Authentication
app.include_router(auth.router)

# User
app.include_router(user.router)

# Train
app.include_router(train.router)

# Passenger
app.include_router(passenger.router)

# Booking
app.include_router(booking.router)

# Payment
app.include_router(payment.router)

# Ticket
app.include_router(ticket.router)

# Seat Availability
app.include_router(availability.router)

# PNR Status
app.include_router(pnr.router)

# Dashboard
app.include_router(dashboard.router)

# =========================
# Home Route
# =========================
@app.get("/")
def home():
    return {
        "message": "Tatkal Assistant API Running Successfully"
    }