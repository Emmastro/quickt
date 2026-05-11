from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_agency_staff
from app.domains.auth.models import User
from app.domains.departures.schemas import DeparturePublic
from app.domains.schedules.schemas import (
    GenerateDeparturesRequest,
    ScheduleCreate,
    ScheduleListResponse,
    SchedulePublic,
    ScheduleUpdate,
)
from app.domains.schedules.service import ScheduleService

router = APIRouter()


@router.post("/", response_model=SchedulePublic, status_code=201)
async def create_schedule(
    data: ScheduleCreate,
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = ScheduleService(db)
    return await svc.create(current_user.agency_id, data.model_dump())


@router.get("/", response_model=ScheduleListResponse)
async def list_schedules(
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = ScheduleService(db)
    schedules = await svc.list(current_user.agency_id)
    return {"items": schedules, "total": len(schedules)}


@router.get("/{schedule_id}", response_model=SchedulePublic)
async def get_schedule(
    schedule_id: int,
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = ScheduleService(db)
    return await svc.get_by_id(schedule_id, current_user.agency_id)


@router.patch("/{schedule_id}", response_model=SchedulePublic)
async def update_schedule(
    schedule_id: int,
    data: ScheduleUpdate,
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = ScheduleService(db)
    return await svc.update(schedule_id, current_user.agency_id, data.model_dump(exclude_unset=True))


@router.post("/{schedule_id}/generate-departures", response_model=list[DeparturePublic])
async def generate_departures(
    schedule_id: int,
    data: GenerateDeparturesRequest,
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = ScheduleService(db)
    return await svc.generate_departures(
        schedule_id, current_user.agency_id, data.from_date, data.to_date
    )
