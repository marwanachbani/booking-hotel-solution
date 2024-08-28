from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Payment(BaseModel):
    payment_id: UUID
    booking_id: UUID
    amount: int  # Amount in cents
    currency: str  # Currency code (e.g., "USD")
    status: str
    created_at: datetime
