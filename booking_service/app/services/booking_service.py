from app.models.booking import Booking
from app.repositories.booking_repository import BookingRepository
from uuid import uuid4, UUID
from typing import List
from datetime import date

class BookingService:

    def __init__(self, repository: BookingRepository):
        self.repository = repository

    def create_booking(self, hotel_id: UUID, user_id: UUID, room_number: int, check_in_date: date, check_out_date: date) -> Booking:
        booking = Booking(
            booking_id=uuid4(),
            hotel_id=hotel_id,
            user_id=user_id,
            room_number=room_number,
            check_in_date=check_in_date,
            check_out_date=check_out_date
        )
        self.repository.add_booking(booking)
        return booking

    def get_bookings_for_hotel(self, hotel_id: UUID) -> List[Booking]:
        return self.repository.get_bookings_by_hotel(hotel_id)

    def get_bookings_for_user(self, user_id: UUID) -> List[Booking]:
        return self.repository.get_bookings_by_user(user_id)