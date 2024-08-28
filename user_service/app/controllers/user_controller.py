from fastapi import APIRouter, Depends, HTTPException, status
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.models.user import User
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class UserOut(BaseModel):
    user_id: UUID
    email: str
    full_name: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

def get_user_service() -> UserService:
    repository = UserRepository()
    return UserService(repository)

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, service: UserService = Depends(get_user_service)):
    existing_user = service.repository.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_user = service.register_user(user.email, user.password, user.full_name)
    return new_user

@router.post("/login", response_model=Token)
def login(email: str, password: str, service: UserService = Depends(get_user_service)):
    token = service.authenticate_user(email, password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
