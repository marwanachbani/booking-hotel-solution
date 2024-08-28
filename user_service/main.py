from fastapi import FastAPI
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.controllers import user_controller
import os

app = FastAPI()
def create_admin_account():
    repository = UserRepository(cassandra_host=os.getenv("CASSANDRA_HOST", "localhost"))
    service = UserService(repository)
    
    # Check if the admin account exists
    if not service.get_user_by_email("adminstrate-2024@example.com"):
        # Create the admin account
        service.register_user(
            email="adminstrate-2024@example.com",
            password="Adminstaration@2024-BGR",
            full_name="Administrator",
            role="admin"
        )

create_admin_account()
# Include routers
app.include_router(user_controller.router)

