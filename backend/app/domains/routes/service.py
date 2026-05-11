from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError

from .models import Route
from .schemas import RouteCreate, RouteUpdate


class RouteService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: RouteCreate) -> Route:
        existing = await self.db.execute(
            select(Route).where(
                Route.origin_city == data.origin_city,
                Route.destination_city == data.destination_city,
            )
        )
        if existing.scalar_one_or_none():
            raise ConflictError("This route already exists")

        route = Route(**data.model_dump())
        self.db.add(route)
        await self.db.flush()
        return route

    async def list(
        self,
        origin: str | None = None,
        destination: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Route], int]:
        query = select(Route).where(Route.is_active.is_(True))
        count_query = select(func.count(Route.id)).where(Route.is_active.is_(True))

        if origin:
            query = query.where(Route.origin_city.ilike(f"%{origin}%"))
            count_query = count_query.where(Route.origin_city.ilike(f"%{origin}%"))
        if destination:
            query = query.where(Route.destination_city.ilike(f"%{destination}%"))
            count_query = count_query.where(Route.destination_city.ilike(f"%{destination}%"))

        total = (await self.db.execute(count_query)).scalar() or 0
        result = await self.db.execute(query.order_by(Route.origin_city).offset(skip).limit(limit))
        return list(result.scalars().all()), total

    async def get_by_id(self, route_id: int) -> Route:
        result = await self.db.execute(select(Route).where(Route.id == route_id))
        route = result.scalar_one_or_none()
        if not route:
            raise NotFoundError("Route")
        return route

    async def update(self, route_id: int, data: RouteUpdate) -> Route:
        route = await self.get_by_id(route_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(route, field, value)
        await self.db.flush()
        return route

    async def get_popular(self, limit: int = 10) -> list[Route]:
        result = await self.db.execute(
            select(Route)
            .where(Route.is_active.is_(True))
            .order_by(Route.origin_city)
            .limit(limit)
        )
        return list(result.scalars().all())
