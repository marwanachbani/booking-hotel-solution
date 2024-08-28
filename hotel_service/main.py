from fastapi import FastAPI
from app.controllers import hotel_controller

app = FastAPI()

# Include routers
app.include_router(hotel_controller.router)
