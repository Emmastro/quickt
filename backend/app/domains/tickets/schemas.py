from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class TicketSeatRequest(BaseModel):
    seat_number: str
    passenger_name: str = Field(..., max_length=255)
    passenger_phone: str = Field(..., max_length=20)


class TicketCreateRequest(BaseModel):
    departure_id: int
    seats: list[TicketSeatRequest] = Field(..., min_length=1, max_length=10)


class TicketPublic(BaseModel):
    id: int
    code: str
    departure_id: int
    seat_number: str
    passenger_name: str
    passenger_phone: str
    status: str
    price: Decimal
    qr_code_url: str | None
    booking_reference: str
    reserved_at: datetime
    confirmed_at: datetime | None
    cancelled_at: datetime | None

    model_config = {"from_attributes": True}


class TicketDetail(TicketPublic):
    origin_city: str = ""
    destination_city: str = ""
    departure_date: str = ""
    departure_time: str = ""
    agency_name: str = ""
    bus_model: str = ""
    cancellation_reason: str | None = None


class TicketCancelRequest(BaseModel):
    reason: str | None = None


class BookingResponse(BaseModel):
    booking_reference: str
    tickets: list[TicketPublic]
    total: Decimal


class TicketListResponse(BaseModel):
    items: list[TicketPublic]
    total: int
