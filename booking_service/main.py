from fastapi import FastAPI
from app.controllers import booking_controller

app = FastAPI()

# Include routers
app.include_router(booking_controller.router)

