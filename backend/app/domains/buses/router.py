from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_agency_staff
from app.domains.auth.models import User
from app.domains.buses.schemas import BusCreate, BusListResponse, BusPublic, BusUpdate
from app.domains.buses.service import BusService

router = APIRouter()


@router.post("/", response_model=BusPublic, status_code=201)
async def create_bus(
    data: BusCreate,
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = BusService(db)
    bus = await svc.create(current_user.agency_id, data.model_dump())
    return bus


@router.get("/", response_model=BusListResponse)
async def list_buses(
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = BusService(db)
    buses = await svc.list(current_user.agency_id)
    return {"items": buses, "total": len(buses)}


@router.get("/{bus_id}", response_model=BusPublic)
async def get_bus(
    bus_id: int,
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = BusService(db)
    return await svc.get_by_id(bus_id, current_user.agency_id)


@router.patch("/{bus_id}", response_model=BusPublic)
async def update_bus(
    bus_id: int,
    data: BusUpdate,
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = BusService(db)
    return await svc.update(bus_id, current_user.agency_id, data.model_dump(exclude_unset=True))


@router.delete("/{bus_id}", status_code=204)
async def delete_bus(
    bus_id: int,
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = BusService(db)
    await svc.delete(bus_id, current_user.agency_id)
