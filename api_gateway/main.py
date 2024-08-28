from fastapi import FastAPI
from app.controllers import hotel_controller, booking_controller, payment_controller, user_controller

app = FastAPI()

# Include routers
app.include_router(hotel_controller.router, prefix="/hotels")
app.include_router(booking_controller.router, prefix="/bookings")
app.include_router(payment_controller.router, prefix="/payments")
app.include_router(user_controller.router, prefix="/users")
