from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PaymentInitiateRequest(BaseModel):
    booking_reference: str
    method: str  # "flooz" or "t_money"
    phone: str = Field(..., max_length=20)


class PaymentPublic(BaseModel):
    id: int
    booking_reference: str
    amount: Decimal
    method: str
    phone: str
    status: str
    provider_tx_id: str | None
    confirmed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class PaymentStatusResponse(BaseModel):
    id: int
    status: str
    booking_reference: str


class WebhookPayload(BaseModel):
    tx_id: str
    status: str  # "success" or "failed"
    reference: str
