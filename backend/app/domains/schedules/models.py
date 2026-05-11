from datetime import datetime, time, timezone
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, JSONBType


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agency_id: Mapped[int] = mapped_column(Integer, ForeignKey("agencies.id"), index=True)
    route_id: Mapped[int] = mapped_column(Integer, ForeignKey("routes.id"), index=True)
    bus_id: Mapped[int] = mapped_column(Integer, ForeignKey("buses.id"), index=True)
    departure_time: Mapped[time] = mapped_column(Time)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    days_of_week: Mapped[list] = mapped_column(
        JSONBType, default=lambda: [0, 1, 2, 3, 4, 5, 6]
    )  # 0=Monday ... 6=Sunday
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
