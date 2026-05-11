from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, NotFoundError
from app.domains.agencies.models import Agency
from app.domains.buses.models import Bus
from app.domains.departures.models import Departure, DepartureStatus
from app.domains.routes.models import Route


class DepartureService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search(
        self,
        origin: str,
        destination: str,
        travel_date: date,
    ) -> list[dict]:
        result = await self.db.execute(
            select(
                Departure,
                Route.origin_city,
                Route.destination_city,
                Route.distance_km,
                Route.estimated_duration_minutes,
                Agency.name.label("agency_name"),
                Bus.model.label("bus_model"),
                Bus.amenities,
            )
            .join(Route, Departure.route_id == Route.id)
            .join(Agency, Departure.agency_id == Agency.id)
            .join(Bus, Departure.bus_id == Bus.id)
            .where(
                Route.origin_city.ilike(origin),
                Route.destination_city.ilike(destination),
                Departure.departure_date == travel_date,
                Departure.status == DepartureStatus.scheduled,
                Departure.available_seats > 0,
            )
            .order_by(Departure.departure_time)
        )

        rows = result.all()
        return [
            {
                "id": row.Departure.id,
                "agency_id": row.Departure.agency_id,
                "agency_name": row.agency_name,
                "route_id": row.Departure.route_id,
                "origin_city": row.origin_city,
                "destination_city": row.destination_city,
                "distance_km": row.distance_km,
                "estimated_duration_minutes": row.estimated_duration_minutes,
                "departure_date": row.Departure.departure_date,
                "departure_time": row.Departure.departure_time,
                "price": row.Departure.price,
                "available_seats": row.Departure.available_seats,
                "total_seats": row.Departure.total_seats,
                "bus_model": row.bus_model,
                "amenities": row.amenities or [],
            }
            for row in rows
        ]

    async def get_by_id(self, departure_id: int) -> Departure:
        result = await self.db.execute(
            select(Departure).where(Departure.id == departure_id)
        )
        departure = result.scalar_one_or_none()
        if not departure:
            raise NotFoundError("Departure not found")
        return departure

    async def get_detail(self, departure_id: int) -> dict:
        result = await self.db.execute(
            select(
                Departure,
                Route.origin_city,
                Route.destination_city,
                Route.distance_km,
                Route.estimated_duration_minutes,
                Agency.name.label("agency_name"),
                Bus.model.label("bus_model"),
                Bus.capacity.label("bus_capacity"),
                Bus.seat_layout,
                Bus.amenities,
            )
            .join(Route, Departure.route_id == Route.id)
            .join(Agency, Departure.agency_id == Agency.id)
            .join(Bus, Departure.bus_id == Bus.id)
            .where(Departure.id == departure_id)
        )
        row = result.one_or_none()
        if not row:
            raise NotFoundError("Departure not found")

        dep = row.Departure
        return {
            "id": dep.id,
            "schedule_id": dep.schedule_id,
            "agency_id": dep.agency_id,
            "route_id": dep.route_id,
            "bus_id": dep.bus_id,
            "departure_date": dep.departure_date,
            "departure_time": dep.departure_time,
            "price": dep.price,
            "status": dep.status,
            "total_seats": dep.total_seats,
            "available_seats": dep.available_seats,
            "booked_seats": dep.booked_seats or [],
            "origin_city": row.origin_city,
            "destination_city": row.destination_city,
            "distance_km": row.distance_km,
            "estimated_duration_minutes": row.estimated_duration_minutes,
            "agency_name": row.agency_name,
            "bus_model": row.bus_model,
            "bus_capacity": row.bus_capacity,
            "seat_layout": row.seat_layout or {},
            "amenities": row.amenities or [],
        }

    async def list_by_agency(self, agency_id: int) -> list[Departure]:
        result = await self.db.execute(
            select(Departure)
            .where(Departure.agency_id == agency_id)
            .order_by(Departure.departure_date.desc(), Departure.departure_time)
        )
        return list(result.scalars().all())

    async def update_status(
        self, departure_id: int, agency_id: int, new_status: str
    ) -> Departure:
        result = await self.db.execute(
            select(Departure).where(
                Departure.id == departure_id, Departure.agency_id == agency_id
            )
        )
        departure = result.scalar_one_or_none()
        if not departure:
            raise NotFoundError("Departure not found")

        valid_transitions = {
            DepartureStatus.scheduled: [DepartureStatus.boarding, DepartureStatus.cancelled],
            DepartureStatus.boarding: [DepartureStatus.departed, DepartureStatus.cancelled],
            DepartureStatus.departed: [DepartureStatus.completed],
        }

        allowed = valid_transitions.get(departure.status, [])
        try:
            target = DepartureStatus(new_status)
        except ValueError:
            raise BadRequestError(f"Invalid status: {new_status}")

        if target not in allowed:
            raise BadRequestError(
                f"Cannot transition from {departure.status.value} to {new_status}"
            )

        departure.status = target
        await self.db.flush()
        await self.db.refresh(departure)
        return departure
