from __future__ import annotations

from datetime import datetime, timezone

from slugify import slugify
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.domains.auth.models import User, UserRole

from .models import Agency, AgencyStatus
from .schemas import AgencyCreate, AgencyUpdate


class AgencyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: AgencyCreate, owner: User) -> Agency:
        # Check name uniqueness
        existing = await self.db.execute(select(Agency).where(Agency.name == data.name))
        if existing.scalar_one_or_none():
            raise ConflictError("An agency with this name already exists")

        agency = Agency(
            name=data.name,
            slug=slugify(data.name),
            description=data.description,
            phone=data.phone,
            email=data.email,
            address=data.address,
            city=data.city,
            region=data.region,
        )
        self.db.add(agency)
        await self.db.flush()

        # Set the owner as agency_staff
        owner.role = UserRole.agency_staff
        owner.agency_id = agency.id
        await self.db.flush()

        return agency

    async def list(
        self,
        region: str | None = None,
        status: str | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 20,
        include_all: bool = False,
    ) -> tuple[list[Agency], int]:
        query = select(Agency)
        count_query = select(func.count(Agency.id))

        if not include_all:
            query = query.where(Agency.status == AgencyStatus.approved)
            count_query = count_query.where(Agency.status == AgencyStatus.approved)

        if status:
            query = query.where(Agency.status == status)
            count_query = count_query.where(Agency.status == status)
        if region:
            query = query.where(Agency.region == region)
            count_query = count_query.where(Agency.region == region)
        if search:
            query = query.where(Agency.name.ilike(f"%{search}%"))
            count_query = count_query.where(Agency.name.ilike(f"%{search}%"))

        total = (await self.db.execute(count_query)).scalar() or 0
        result = await self.db.execute(
            query.order_by(Agency.created_at.desc()).offset(skip).limit(limit)
        )
        return list(result.scalars().all()), total

    async def get_by_id(self, agency_id: int) -> Agency:
        result = await self.db.execute(select(Agency).where(Agency.id == agency_id))
        agency = result.scalar_one_or_none()
        if not agency:
            raise NotFoundError("Agency")
        return agency

    async def get_by_slug(self, slug: str) -> Agency:
        result = await self.db.execute(select(Agency).where(Agency.slug == slug))
        agency = result.scalar_one_or_none()
        if not agency:
            raise NotFoundError("Agency")
        return agency

    async def update(self, agency_id: int, data: AgencyUpdate, user: User) -> Agency:
        agency = await self.get_by_id(agency_id)
        if user.role != "admin" and user.agency_id != agency_id:
            raise ForbiddenError("You can only update your own agency")

        for field, value in data.model_dump(exclude_unset=True).items():
            if field == "name" and value:
                agency.slug = slugify(value)
            setattr(agency, field, value)
        await self.db.flush()
        return agency

    async def approve(self, agency_id: int) -> Agency:
        agency = await self.get_by_id(agency_id)
        agency.status = AgencyStatus.approved
        agency.approved_at = datetime.now(timezone.utc)
        await self.db.flush()
        return agency

    async def suspend(self, agency_id: int) -> Agency:
        agency = await self.get_by_id(agency_id)
        agency.status = AgencyStatus.suspended
        await self.db.flush()
        return agency
