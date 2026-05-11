from datetime import date, time
from decimal import Decimal

from pydantic import BaseModel, Field


class ScheduleCreate(BaseModel):
    route_id: int
    bus_id: int
    departure_time: time
    price: Decimal = Field(..., gt=0)
    days_of_week: list[int] = Field(default=[0, 1, 2, 3, 4, 5, 6])


class ScheduleUpdate(BaseModel):
    route_id: int | None = None
    bus_id: int | None = None
    departure_time: time | None = None
    price: Decimal | None = None
    days_of_week: list[int] | None = None
    is_active: bool | None = None


class SchedulePublic(BaseModel):
    id: int
    agency_id: int
    route_id: int
    bus_id: int
    departure_time: time
    price: Decimal
    days_of_week: list[int]
    is_active: bool

    model_config = {"from_attributes": True}


class ScheduleListResponse(BaseModel):
    items: list[SchedulePublic]
    total: int


class GenerateDeparturesRequest(BaseModel):
    from_date: date
    to_date: date
