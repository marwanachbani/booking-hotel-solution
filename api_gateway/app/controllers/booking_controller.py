from fastapi import APIRouter, Depends, HTTPException
import httpx
from uuid import UUID
from app.config.security import get_current_user_role, verify_admin

router = APIRouter()

BOOKING_SERVICE_URL = "http://booking_service:8002"

@router.post("/bookings", response_model=dict, dependencies=[Depends(get_current_user_role)])
async def create_booking(
    hotel_id: UUID,
    user_id: UUID,
    room_number: int,
    check_in_date: str,
    check_out_date: str
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BOOKING_SERVICE_URL}/bookings",
            params={
                "hotel_id": hotel_id,
                "user_id": user_id,
                "room_number": room_number,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date
            },
        )
        return response.json()

@router.post("/bookings/{booking_id}/accept", dependencies=[Depends(verify_admin)])
async def accept_booking(booking_id: UUID):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BOOKING_SERVICE_URL}/bookings/{booking_id}/accept")
        return response.json()

@router.post("/bookings/{booking_id}/deny", dependencies=[Depends(verify_admin)])
async def deny_booking(booking_id: UUID):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BOOKING_SERVICE_URL}/bookings/{booking_id}/deny")
        return response.json()
