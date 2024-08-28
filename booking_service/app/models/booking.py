from pydantic import BaseModel
from uuid import UUID
from datetime import date
class Booking(BaseModel):
    booking_id: UUID
    hotel_id: UUID
    user_id: UUID
    room_number: int
    check_in_date: date
    check_out_date: date