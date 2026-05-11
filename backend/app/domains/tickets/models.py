import enum
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TicketStatus(str, enum.Enum):
    reserved = "reserved"
    confirmed = "confirmed"
    cancelled = "cancelled"
    used = "used"
    expired = "expired"


class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        UniqueConstraint("departure_id", "seat_number", name="uq_ticket_departure_seat"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    departure_id: Mapped[int] = mapped_column(Integer, ForeignKey("departures.id"), index=True)
    customer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    seat_number: Mapped[str] = mapped_column(String(10))
    passenger_name: Mapped[str] = mapped_column(String(255))
    passenger_phone: Mapped[str] = mapped_column(String(20))
    status: Mapped[TicketStatus] = mapped_column(
        SAEnum(TicketStatus, name="ticket_status_enum", create_constraint=False),
        default=TicketStatus.reserved,
    )
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    qr_code_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    booking_reference: Mapped[str] = mapped_column(String(20), index=True)
    reserved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
