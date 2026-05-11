from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_admin

from .models import Agency
from .schemas import AgencyCreate, AgencyListResponse, AgencyPublic, AgencyUpdate
from .service import AgencyService
from app.domains.auth.models import User

router = APIRouter()


@router.post("/", response_model=AgencyPublic, status_code=201)
async def create_agency(
    data: AgencyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    svc = AgencyService(db)
    return await svc.create(data, current_user)


@router.get("/", response_model=AgencyListResponse)
async def list_agencies(
    region: str | None = None,
    status: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    svc = AgencyService(db)
    items, total = await svc.list(region=region, status=status, search=search, skip=skip, limit=limit)
    return AgencyListResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{agency_id}", response_model=AgencyPublic)
async def get_agency(agency_id: int, db: AsyncSession = Depends(get_db)):
    svc = AgencyService(db)
    return await svc.get_by_id(agency_id)


@router.patch("/{agency_id}", response_model=AgencyPublic)
async def update_agency(
    agency_id: int,
    data: AgencyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    svc = AgencyService(db)
    return await svc.update(agency_id, data, current_user)


@router.patch("/{agency_id}/approve", response_model=AgencyPublic)
async def approve_agency(
    agency_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    svc = AgencyService(db)
    return await svc.approve(agency_id)


@router.patch("/{agency_id}/suspend", response_model=AgencyPublic)
async def suspend_agency(
    agency_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    svc = AgencyService(db)
    return await svc.suspend(agency_id)
