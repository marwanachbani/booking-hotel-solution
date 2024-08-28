from pydantic import BaseModel
from uuid import UUID

class Hotel(BaseModel):
    hotel_id: UUID
    name: str
    address: str
    rooms: int