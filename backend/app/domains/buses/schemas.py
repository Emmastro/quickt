from pydantic import BaseModel, Field


class SeatLayout(BaseModel):
    rows: int = 10
    seats_per_row: int = 4
    aisle_after_column: int = 2
    unavailable_seats: list[str] = []
    labels: list[str] = []


class BusCreate(BaseModel):
    plate_number: str = Field(..., max_length=20)
    model: str = Field(..., max_length=100)
    capacity: int = Field(..., gt=0)
    seat_layout: SeatLayout = Field(default_factory=SeatLayout)
    amenities: list[str] = []
    image_url: str | None = None


class BusUpdate(BaseModel):
    plate_number: str | None = None
    model: str | None = None
    capacity: int | None = None
    seat_layout: SeatLayout | None = None
    amenities: list[str] | None = None
    image_url: str | None = None
    is_active: bool | None = None


class BusPublic(BaseModel):
    id: int
    agency_id: int
    plate_number: str
    model: str
    capacity: int
    seat_layout: dict
    amenities: list
    image_url: str | None
    is_active: bool

    model_config = {"from_attributes": True}


class BusListResponse(BaseModel):
    items: list[BusPublic]
    total: int
