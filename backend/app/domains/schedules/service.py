from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, NotFoundError
from app.domains.buses.models import Bus
from app.domains.departures.models import Departure, DepartureStatus
from app.domains.schedules.models import Schedule


class ScheduleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, agency_id: int, data: dict) -> Schedule:
        # Verify bus belongs to agency
        result = await self.db.execute(
            select(Bus).where(Bus.id == data["bus_id"], Bus.agency_id == agency_id)
        )
        if not result.scalar_one_or_none():
            raise BadRequestError("Bus not found or does not belong to your agency")

        schedule = Schedule(agency_id=agency_id, **data)
        self.db.add(schedule)
        await self.db.flush()
        await self.db.refresh(schedule)
        return schedule

    async def list(self, agency_id: int) -> list[Schedule]:
        result = await self.db.execute(
            select(Schedule)
            .where(Schedule.agency_id == agency_id)
            .order_by(Schedule.departure_time)
        )
        return list(result.scalars().all())

    async def get_by_id(self, schedule_id: int, agency_id: int | None = None) -> Schedule:
        query = select(Schedule).where(Schedule.id == schedule_id)
        if agency_id is not None:
            query = query.where(Schedule.agency_id == agency_id)
        result = await self.db.execute(query)
        schedule = result.scalar_one_or_none()
        if not schedule:
            raise NotFoundError("Schedule not found")
        return schedule

    async def update(self, schedule_id: int, agency_id: int, data: dict) -> Schedule:
        schedule = await self.get_by_id(schedule_id, agency_id)
        update_data = {k: v for k, v in data.items() if v is not None}
        for key, value in update_data.items():
            setattr(schedule, key, value)
        await self.db.flush()
        await self.db.refresh(schedule)
        return schedule

    async def generate_departures(
        self, schedule_id: int, agency_id: int, from_date: date, to_date: date
    ) -> list[Departure]:
        if from_date > to_date:
            raise BadRequestError("from_date must be before to_date")
        if (to_date - from_date).days > 90:
            raise BadRequestError("Cannot generate departures for more than 90 days")

        schedule = await self.get_by_id(schedule_id, agency_id)
        bus_result = await self.db.execute(select(Bus).where(Bus.id == schedule.bus_id))
        bus = bus_result.scalar_one_or_none()
        if not bus:
            raise BadRequestError("Bus not found for this schedule")

        created = []
        current_date = from_date
        while current_date <= to_date:
            # Check if this day of week is in the schedule
            if current_date.weekday() in schedule.days_of_week:
                # Check if departure already exists
                exists = await self.db.execute(
                    select(Departure).where(
                        Departure.schedule_id == schedule.id,
                        Departure.departure_date == current_date,
                    )
                )
                if not exists.scalar_one_or_none():
                    departure = Departure(
                        schedule_id=schedule.id,
                        agency_id=schedule.agency_id,
                        route_id=schedule.route_id,
                        bus_id=schedule.bus_id,
                        departure_date=current_date,
                        departure_time=schedule.departure_time,
                        price=schedule.price,
                        status=DepartureStatus.scheduled,
                        total_seats=bus.capacity,
                        available_seats=bus.capacity,
                        booked_seats=[],
                    )
                    self.db.add(departure)
                    created.append(departure)

            current_date += timedelta(days=1)

        await self.db.flush()
        for dep in created:
            await self.db.refresh(dep)
        return created
