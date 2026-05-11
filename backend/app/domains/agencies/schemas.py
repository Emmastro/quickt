from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class AgencyCreate(BaseModel):
    name: str
    description: str | None = None
    phone: str
    email: str
    address: str
    city: str
    region: str


class AgencyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    city: str | None = None
    region: str | None = None


class AgencyPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: str | None
    logo_url: str | None
    phone: str
    email: str
    address: str
    city: str
    region: str
    status: str
    rating: Decimal
    is_active: bool
    created_at: datetime
    approved_at: datetime | None


class AgencyListResponse(BaseModel):
    items: list[AgencyPublic]
    total: int
    skip: int
    limit: int
