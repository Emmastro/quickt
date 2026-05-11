from datetime import date, datetime

from pydantic import BaseModel


class TripCreate(BaseModel):
    route_id: int
    planned_date: date
    notes: str | None = None
    reminder_hours_before: int = 24


class TripUpdate(BaseModel):
    planned_date: date | None = None
    notes: str | None = None
    reminder_hours_before: int | None = None


class TripPublic(BaseModel):
    id: int
    route_id: int
    planned_date: date
    notes: str | None
    reminder_hours_before: int
    reminder_sent: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TripDetail(TripPublic):
    origin_city: str = ""
    destination_city: str = ""
    distance_km: int | None = None
    estimated_duration_minutes: int = 0


class TripListResponse(BaseModel):
    items: list[TripPublic]
    total: int
