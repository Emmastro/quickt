from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.domains.auth.models import User
from app.domains.payments.schemas import (
    PaymentInitiateRequest,
    PaymentPublic,
    PaymentStatusResponse,
    WebhookPayload,
)
from app.domains.payments.service import PaymentService

router = APIRouter()


@router.post("/initiate", response_model=PaymentPublic, status_code=201)
async def initiate_payment(
    data: PaymentInitiateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = PaymentService(db)
    return await svc.initiate(data.booking_reference, data.method, data.phone)


@router.post("/webhook", response_model=PaymentPublic)
async def payment_webhook(
    data: WebhookPayload,
    db: AsyncSession = Depends(get_db),
):
    svc = PaymentService(db)
    return await svc.handle_webhook(data.tx_id, data.status, data.reference)


@router.get("/{payment_id}/status", response_model=PaymentStatusResponse)
async def get_payment_status(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = PaymentService(db)
    payment = await svc.get_status(payment_id)
    return {
        "id": payment.id,
        "status": payment.status,
        "booking_reference": payment.booking_reference,
    }


@router.get("/my", response_model=list[PaymentPublic])
async def get_my_payments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = PaymentService(db)
    return await svc.get_customer_payments(current_user.id)
