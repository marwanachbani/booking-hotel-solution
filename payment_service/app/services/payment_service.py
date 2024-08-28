from app.models.payment import Payment
from app.repositories.payment_repository import PaymentRepository
from app.configs.square_client import get_square_client
from uuid import uuid4, UUID
from datetime import datetime
from typing import List

class PaymentService:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository
        self.square_client = get_square_client()

    def create_payment(self, booking_id: UUID, amount: int, currency: str, source_id: str,
                       app_fee_amount: int = 0, autocomplete: bool = True, customer_id: str = None,
                       location_id: str = None, reference_id: str = None, note: str = None) -> Payment:
        body = {
            "source_id": source_id,
            "idempotency_key": str(uuid4()),  # Unique key for preventing duplicate charges
            "amount_money": {
                "amount": amount,
                "currency": currency
            },
            "app_fee_money": {
                "amount": app_fee_amount,
                "currency": currency
            } if app_fee_amount else None,
            "autocomplete": autocomplete,
            "customer_id": customer_id,
            "location_id": location_id,
            "reference_id": reference_id,
            "note": note
        }

        # Remove None values from the body
        body = {k: v for k, v in body.items() if v is not None}

        result = self.square_client.payments.create_payment(body)

