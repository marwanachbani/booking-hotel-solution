from fastapi import APIRouter
import httpx
from uuid import UUID

router = APIRouter()

PAYMENT_SERVICE_URL = "http://0.0.0.0:8003"

@router.post("/payments", response_model=dict)
async def create_payment(
    booking_id: UUID,
    amount: int,
    currency: str,
    source_id: str,
    customer_id: str = None,
    location_id: str = None,
    note: str = None
):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYMENT_SERVICE_URL}/payments",
            params={
                "booking_id": booking_id,
                "amount": amount,
                "currency": currency,
                "source_id": source_id,
                "customer_id": customer_id,
                "location_id": location_id,
                "note": note,
            },
        )
        return response.json()
