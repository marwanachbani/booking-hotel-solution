from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from app.services.payment_service import PaymentService
from app.repositories.payment_repository import PaymentRepository
from app.models.payment import Payment
from typing import List

router = APIRouter()

# Dependency injection
def get_payment_service() -> PaymentService:
    repository = PaymentRepository()
    return PaymentService(repository)

@router.post("/payments", response_model=Payment)
def create_payment(
    booking_id: UUID,
    amount: int,  # Amount in cents
    currency: str,
    source_id: str,  # Source ID (e.g., card nonce) from Square's frontend SDK
    service: PaymentService = Depends(get_payment_service)
):
    try:
        return service.create_payment(booking_id, amount, currency, source_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/payments/{payment_id}", response_model=Payment)
def get_payment(payment_id: UUID, service: PaymentService = Depends(get_payment_service)):
    payment = service.get_payment(payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.get("/bookings/{booking_id}/payments", response_model=List[Payment])
def get_payments_by_booking(booking_id: UUID, service: PaymentService = Depends(get_payment_service)):
    return service.get_payments_by_booking(booking_id)
