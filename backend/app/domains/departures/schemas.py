from datetime import date, time
from decimal import Decimal

from pydantic import BaseModel


class DeparturePublic(BaseModel):
    id: int
    schedule_id: int
    agency_id: int
    route_id: int
    bus_id: int
    departure_date: date
    departure_time: time
    price: Decimal
    status: str
    total_seats: int
    available_seats: int
    booked_seats: list[str]

    model_config = {"from_attributes": True}


class DepartureSearchResult(BaseModel):
    id: int
    agency_id: int
    agency_name: str
    route_id: int
    origin_city: str
    destination_city: str
    distance_km: int | None
    estimated_duration_minutes: int
    departure_date: date
    departure_time: time
    price: Decimal
    available_seats: int
    total_seats: int
    bus_model: str
    amenities: list


class DepartureDetail(DeparturePublic):
    origin_city: str = ""
    destination_city: str = ""
    distance_km: int | None = None
    estimated_duration_minutes: int = 0
    agency_name: str = ""
    bus_model: str = ""
    bus_capacity: int = 0
    seat_layout: dict = {}
    amenities: list = []


class DepartureStatusUpdate(BaseModel):
    status: str


class DepartureListResponse(BaseModel):
    items: list[DeparturePublic]
    total: int
