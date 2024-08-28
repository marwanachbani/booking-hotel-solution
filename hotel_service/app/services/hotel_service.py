from app.models.hotel import Hotel
from app.repositories.hotel_repository import HotelRepository
from uuid import uuid4
from typing import List

class HotelService:

    def __init__(self, repository: HotelRepository):
        self.repository = repository

    def create_hotel(self, name: str, address: str, rooms: int) -> Hotel:
        hotel = Hotel(hotel_id=uuid4(), name=name, address=address, rooms=rooms)
        self.repository.add_hotel(hotel)
        return hotel

    def list_hotels(self) -> List[Hotel]:
        return self.repository.get_hotels()
