from datetime import datetime

from pydantic import BaseModel, ConfigDict, computed_field


class RouteCreate(BaseModel):
    origin_city: str
    destination_city: str
    distance_km: int | None = None
    estimated_duration_minutes: int


class RouteUpdate(BaseModel):
    origin_city: str | None = None
    destination_city: str | None = None
    distance_km: int | None = None
    estimated_duration_minutes: int | None = None
    is_active: bool | None = None


class RoutePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    origin_city: str
    destination_city: str
    distance_km: int | None
    estimated_duration_minutes: int
    is_active: bool
    created_at: datetime

    @computed_field
    @property
    def duration_display(self) -> str:
        hours = self.estimated_duration_minutes // 60
        mins = self.estimated_duration_minutes % 60
        if hours and mins:
            return f"{hours}h {mins}min"
        elif hours:
            return f"{hours}h"
        return f"{mins}min"


class RouteListResponse(BaseModel):
    items: list[RoutePublic]
    total: int
    skip: int
    limit: int
