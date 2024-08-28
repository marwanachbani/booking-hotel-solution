from fastapi import FastAPI
from app.controllers import payment_controller

app = FastAPI()

# Include routers
app.include_router(payment_controller.router)
