from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError, NotFoundError
from app.core.qr import generate_ticket_qr
from app.core.security import generate_booking_reference, generate_ticket_code
from app.domains.agencies.models import Agency
from app.domains.buses.models import Bus
from app.domains.departures.models import Departure, DepartureStatus
from app.domains.routes.models import Route
from app.domains.tickets.models import Ticket, TicketStatus

RESERVATION_EXPIRY_MINUTES = 15


class TicketService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _expire_stale_reservations(self, departure_id: int) -> None:
        """Expire reservations older than 15 minutes."""
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=RESERVATION_EXPIRY_MINUTES)
        result = await self.db.execute(
            select(Ticket).where(
                Ticket.departure_id == departure_id,
                Ticket.status == TicketStatus.reserved,
                Ticket.reserved_at < cutoff,
            )
        )
        stale_tickets = result.scalars().all()
        if not stale_tickets:
            return

        departure = await self.db.execute(
            select(Departure).where(Departure.id == departure_id)
        )
        dep = departure.scalar_one()

        for ticket in stale_tickets:
            ticket.status = TicketStatus.expired
            if ticket.seat_number in dep.booked_seats:
                dep.booked_seats = [s for s in dep.booked_seats if s != ticket.seat_number]
                dep.available_seats += 1

        await self.db.flush()

    async def reserve(
        self,
        customer_id: uuid.UUID,
        departure_id: int,
        seats: list[dict],
    ) -> tuple[str, list[Ticket]]:
        # Expire stale reservations first
        await self._expire_stale_reservations(departure_id)

        dep_result = await self.db.execute(
            select(Departure).where(Departure.id == departure_id)
        )
        departure = dep_result.scalar_one_or_none()
        if not departure:
            raise NotFoundError("Departure not found")

        if departure.status != DepartureStatus.scheduled:
            raise BadRequestError("This departure is no longer accepting reservations")

        if len(seats) > departure.available_seats:
            raise BadRequestError("Not enough seats available")

        booking_ref = generate_booking_reference()
        created_tickets = []
        booked = list(departure.booked_seats or [])

        for seat_data in seats:
            seat_number = seat_data["seat_number"]
            if seat_number in booked:
                raise ConflictError(f"Seat {seat_number} is already taken")

            # Check DB-level uniqueness
            existing = await self.db.execute(
                select(Ticket).where(
                    Ticket.departure_id == departure_id,
                    Ticket.seat_number == seat_number,
                    Ticket.status.in_([TicketStatus.reserved, TicketStatus.confirmed]),
                )
            )
            if existing.scalar_one_or_none():
                raise ConflictError(f"Seat {seat_number} is already reserved")

            ticket = Ticket(
                code=generate_ticket_code(),
                departure_id=departure_id,
                customer_id=customer_id,
                seat_number=seat_number,
                passenger_name=seat_data["passenger_name"],
                passenger_phone=seat_data["passenger_phone"],
                status=TicketStatus.reserved,
                price=departure.price,
                booking_reference=booking_ref,
            )
            self.db.add(ticket)
            created_tickets.append(ticket)
            booked.append(seat_number)

        departure.booked_seats = booked
        departure.available_seats -= len(seats)

        await self.db.flush()
        for t in created_tickets:
            await self.db.refresh(t)

        return booking_ref, created_tickets

    async def confirm_tickets(self, booking_reference: str) -> list[Ticket]:
        """Confirm all tickets in a booking (called after payment success)."""
        result = await self.db.execute(
            select(Ticket).where(
                Ticket.booking_reference == booking_reference,
                Ticket.status == TicketStatus.reserved,
            )
        )
        tickets = list(result.scalars().all())
        if not tickets:
            raise NotFoundError("No reserved tickets found for this booking")

        now = datetime.now(timezone.utc)
        for ticket in tickets:
            ticket.status = TicketStatus.confirmed
            ticket.confirmed_at = now
            ticket.qr_code_url = generate_ticket_qr(ticket.code)

        await self.db.flush()
        for t in tickets:
            await self.db.refresh(t)
        return tickets

    async def get_customer_tickets(self, customer_id: uuid.UUID) -> list[Ticket]:
        result = await self.db.execute(
            select(Ticket)
            .where(Ticket.customer_id == customer_id)
            .order_by(Ticket.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, ticket_id: int, customer_id: uuid.UUID | None = None) -> Ticket:
        query = select(Ticket).where(Ticket.id == ticket_id)
        if customer_id:
            query = query.where(Ticket.customer_id == customer_id)
        result = await self.db.execute(query)
        ticket = result.scalar_one_or_none()
        if not ticket:
            raise NotFoundError("Ticket not found")
        return ticket

    async def get_ticket_detail(self, ticket_id: int, customer_id: uuid.UUID) -> dict:
        result = await self.db.execute(
            select(
                Ticket,
                Departure.departure_date,
                Departure.departure_time,
                Route.origin_city,
                Route.destination_city,
                Agency.name.label("agency_name"),
                Bus.model.label("bus_model"),
            )
            .join(Departure, Ticket.departure_id == Departure.id)
            .join(Route, Departure.route_id == Route.id)
            .join(Agency, Departure.agency_id == Agency.id)
            .join(Bus, Departure.bus_id == Bus.id)
            .where(Ticket.id == ticket_id, Ticket.customer_id == customer_id)
        )
        row = result.one_or_none()
        if not row:
            raise NotFoundError("Ticket not found")

        ticket = row.Ticket
        return {
            "id": ticket.id,
            "code": ticket.code,
            "departure_id": ticket.departure_id,
            "seat_number": ticket.seat_number,
            "passenger_name": ticket.passenger_name,
            "passenger_phone": ticket.passenger_phone,
            "status": ticket.status,
            "price": ticket.price,
            "qr_code_url": ticket.qr_code_url,
            "booking_reference": ticket.booking_reference,
            "reserved_at": ticket.reserved_at,
            "confirmed_at": ticket.confirmed_at,
            "cancelled_at": ticket.cancelled_at,
            "cancellation_reason": ticket.cancellation_reason,
            "departure_date": str(row.departure_date),
            "departure_time": str(row.departure_time),
            "origin_city": row.origin_city,
            "destination_city": row.destination_city,
            "agency_name": row.agency_name,
            "bus_model": row.bus_model,
        }

    async def get_by_code(self, code: str) -> Ticket:
        result = await self.db.execute(select(Ticket).where(Ticket.code == code))
        ticket = result.scalar_one_or_none()
        if not ticket:
            raise NotFoundError("Ticket not found")
        return ticket

    async def cancel(
        self, ticket_id: int, customer_id: uuid.UUID, reason: str | None = None
    ) -> Ticket:
        ticket = await self.get_by_id(ticket_id, customer_id)
        if ticket.status not in (TicketStatus.reserved, TicketStatus.confirmed):
            raise BadRequestError("Only reserved or confirmed tickets can be cancelled")

        ticket.status = TicketStatus.cancelled
        ticket.cancelled_at = datetime.now(timezone.utc)
        ticket.cancellation_reason = reason

        # Free the seat
        dep_result = await self.db.execute(
            select(Departure).where(Departure.id == ticket.departure_id)
        )
        departure = dep_result.scalar_one()
        departure.booked_seats = [
            s for s in departure.booked_seats if s != ticket.seat_number
        ]
        departure.available_seats += 1

        await self.db.flush()
        await self.db.refresh(ticket)
        return ticket

    async def mark_used(self, ticket_id: int, agency_id: int) -> Ticket:
        """Agency marks ticket as used (scanned at boarding)."""
        result = await self.db.execute(
            select(Ticket)
            .join(Departure, Ticket.departure_id == Departure.id)
            .where(Ticket.id == ticket_id, Departure.agency_id == agency_id)
        )
        ticket = result.scalar_one_or_none()
        if not ticket:
            raise NotFoundError("Ticket not found")

        if ticket.status != TicketStatus.confirmed:
            raise BadRequestError("Only confirmed tickets can be marked as used")

        ticket.status = TicketStatus.used
        await self.db.flush()
        await self.db.refresh(ticket)
        return ticket

    async def get_departure_passengers(
        self, departure_id: int, agency_id: int
    ) -> list[Ticket]:
        result = await self.db.execute(
            select(Ticket)
            .join(Departure, Ticket.departure_id == Departure.id)
            .where(
                Ticket.departure_id == departure_id,
                Departure.agency_id == agency_id,
                Ticket.status.in_([
                    TicketStatus.reserved, TicketStatus.confirmed, TicketStatus.used
                ]),
            )
            .order_by(Ticket.seat_number)
        )
        return list(result.scalars().all())
