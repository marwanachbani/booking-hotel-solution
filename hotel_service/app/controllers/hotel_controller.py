from fastapi import APIRouter, Depends
from app.services.hotel_service import HotelService
from app.repositories.hotel_repository import HotelRepository
from app.models.hotel import Hotel
from typing import List
import os

router = APIRouter()

# Dependency injection
def get_hotel_service() -> HotelService:
    repository = HotelRepository(cassandra_host=os.getenv("CASSANDRA_HOST", "localhost"))
    return HotelService(repository)

@router.get("/hotels", response_model=List[Hotel])
def get_hotels(service: HotelService = Depends(get_hotel_service)):
    return service.list_hotels()

@router.post("/hotels", response_model=Hotel)
def add_hotel(name: str, address: str, rooms: int, service: HotelService = Depends(get_hotel_service)):
    return service.create_hotel(name, address, rooms)
