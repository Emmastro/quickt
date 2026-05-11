from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.domains.buses.models import Bus


class BusService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, agency_id: int, data: dict) -> Bus:
        existing = await self.db.execute(
            select(Bus).where(Bus.plate_number == data["plate_number"])
        )
        if existing.scalar_one_or_none():
            raise ConflictError("A bus with this plate number already exists")

        if "seat_layout" in data and hasattr(data["seat_layout"], "model_dump"):
            data["seat_layout"] = data["seat_layout"].model_dump()

        bus = Bus(agency_id=agency_id, **data)
        self.db.add(bus)
        await self.db.flush()
        await self.db.refresh(bus)
        return bus

    async def list(self, agency_id: int) -> list[Bus]:
        result = await self.db.execute(
            select(Bus).where(Bus.agency_id == agency_id).order_by(Bus.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, bus_id: int, agency_id: int | None = None) -> Bus:
        query = select(Bus).where(Bus.id == bus_id)
        if agency_id is not None:
            query = query.where(Bus.agency_id == agency_id)
        result = await self.db.execute(query)
        bus = result.scalar_one_or_none()
        if not bus:
            raise NotFoundError("Bus not found")
        return bus

    async def update(self, bus_id: int, agency_id: int, data: dict) -> Bus:
        bus = await self.get_by_id(bus_id, agency_id)
        update_data = {k: v for k, v in data.items() if v is not None}

        if "seat_layout" in update_data and hasattr(update_data["seat_layout"], "model_dump"):
            update_data["seat_layout"] = update_data["seat_layout"].model_dump()

        for key, value in update_data.items():
            setattr(bus, key, value)

        await self.db.flush()
        await self.db.refresh(bus)
        return bus

    async def delete(self, bus_id: int, agency_id: int) -> None:
        bus = await self.get_by_id(bus_id, agency_id)
        await self.db.delete(bus)
        await self.db.flush()
