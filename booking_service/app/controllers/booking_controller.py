from fastapi import APIRouter, Depends, HTTPException
from app.services.booking_service import BookingService
from app.repositories.booking_repository import BookingRepository
from app.models.booking import Booking
from typing import List
from uuid import UUID
from datetime import date
import os

router = APIRouter()

# Dependency injection
def get_booking_service() -> BookingService:
    repository = BookingRepository(cassandra_host=os.getenv("CASSANDRA_HOST", "localhost"))
    return BookingService(repository)

@router.post("/bookings", response_model=Booking)
def create_booking(
    hotel_id: UUID,
    user_id: UUID,
    room_number: int,
    check_in_date: date,
    check_out_date: date,
    service: BookingService = Depends(get_booking_service)
):
    return service.create_booking(hotel_id, user_id, room_number, check_in_date, check_out_date)

@router.get("/bookings/hotel/{hotel_id}", response_model=List[Booking])
def get_bookings_for_hotel(hotel_id: UUID, service: BookingService = Depends(get_booking_service)):
    return service.get_bookings_for_hotel(hotel_id)

@router.get("/bookings/user/{user_id}", response_model=List[Booking])
def get_bookings_for_user(user_id: UUID, service: BookingService = Depends(get_booking_service)):
    return service.get_bookings_for_user(user_id)
