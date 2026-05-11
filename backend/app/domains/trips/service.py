from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.domains.routes.models import Route
from app.domains.trips.models import Trip


class TripService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, customer_id: uuid.UUID, data: dict) -> Trip:
        trip = Trip(customer_id=customer_id, **data)
        self.db.add(trip)
        await self.db.flush()
        await self.db.refresh(trip)
        return trip

    async def list(self, customer_id: uuid.UUID) -> list[dict]:
        result = await self.db.execute(
            select(
                Trip,
                Route.origin_city,
                Route.destination_city,
                Route.distance_km,
                Route.estimated_duration_minutes,
            )
            .join(Route, Trip.route_id == Route.id)
            .where(Trip.customer_id == customer_id)
            .order_by(Trip.planned_date)
        )
        return [
            {
                "id": row.Trip.id,
                "route_id": row.Trip.route_id,
                "planned_date": row.Trip.planned_date,
                "notes": row.Trip.notes,
                "reminder_hours_before": row.Trip.reminder_hours_before,
                "reminder_sent": row.Trip.reminder_sent,
                "created_at": row.Trip.created_at,
                "origin_city": row.origin_city,
                "destination_city": row.destination_city,
                "distance_km": row.distance_km,
                "estimated_duration_minutes": row.estimated_duration_minutes,
            }
            for row in result.all()
        ]

    async def get_by_id(self, trip_id: int, customer_id: uuid.UUID) -> Trip:
        result = await self.db.execute(
            select(Trip).where(Trip.id == trip_id, Trip.customer_id == customer_id)
        )
        trip = result.scalar_one_or_none()
        if not trip:
            raise NotFoundError("Trip not found")
        return trip

    async def update(self, trip_id: int, customer_id: uuid.UUID, data: dict) -> Trip:
        trip = await self.get_by_id(trip_id, customer_id)
        update_data = {k: v for k, v in data.items() if v is not None}
        for key, value in update_data.items():
            setattr(trip, key, value)
        await self.db.flush()
        await self.db.refresh(trip)
        return trip

    async def delete(self, trip_id: int, customer_id: uuid.UUID) -> None:
        trip = await self.get_by_id(trip_id, customer_id)
        await self.db.delete(trip)
        await self.db.flush()
