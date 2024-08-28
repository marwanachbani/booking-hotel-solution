from fastapi import APIRouter, HTTPException, Depends
import httpx
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

router = APIRouter()

USER_SERVICE_URL = "http://user_service:8004"

# Request models
class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class UserOut(BaseModel):
    user_id: UUID
    email: str
    full_name: str
    created_at: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Endpoints

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{USER_SERVICE_URL}/register", json=user.dict())
        if response.status_code == 400:
            raise HTTPException(status_code=400, detail="Email already registered")
        return response.json()

@router.post("/login", response_model=Token)
async def login(email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{USER_SERVICE_URL}/login", 
            data={"email": email, "password": password}
        )
        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return response.json()

@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: UUID):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{USER_SERVICE_URL}/users/{user_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        return response.json()
