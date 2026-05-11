import enum
from datetime import date, datetime, time, timezone
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Time,
    UniqueConstraint,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, JSONBType


class DepartureStatus(str, enum.Enum):
    scheduled = "scheduled"
    boarding = "boarding"
    departed = "departed"
    completed = "completed"
    cancelled = "cancelled"


class Departure(Base):
    __tablename__ = "departures"
    __table_args__ = (
        UniqueConstraint("schedule_id", "departure_date", name="uq_departure_schedule_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    schedule_id: Mapped[int] = mapped_column(Integer, ForeignKey("schedules.id"), index=True)
    agency_id: Mapped[int] = mapped_column(Integer, ForeignKey("agencies.id"), index=True)
    route_id: Mapped[int] = mapped_column(Integer, ForeignKey("routes.id"), index=True)
    bus_id: Mapped[int] = mapped_column(Integer, ForeignKey("buses.id"))
    departure_date: Mapped[date] = mapped_column(Date, index=True)
    departure_time: Mapped[time] = mapped_column(Time)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    status: Mapped[DepartureStatus] = mapped_column(
        SAEnum(DepartureStatus, name="departure_status_enum", create_constraint=False),
        default=DepartureStatus.scheduled,
    )
    total_seats: Mapped[int] = mapped_column(Integer)
    available_seats: Mapped[int] = mapped_column(Integer)
    booked_seats: Mapped[list] = mapped_column(JSONBType, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
