from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_agency_staff
from app.domains.auth.models import User
from app.domains.departures.schemas import (
    DepartureDetail,
    DepartureListResponse,
    DeparturePublic,
    DepartureSearchResult,
    DepartureStatusUpdate,
)
from app.domains.departures.service import DepartureService

router = APIRouter()


@router.get("/search", response_model=list[DepartureSearchResult])
async def search_departures(
    origin: str = Query(...),
    destination: str = Query(...),
    date: date = Query(..., alias="date"),
    db: AsyncSession = Depends(get_db),
):
    svc = DepartureService(db)
    return await svc.search(origin, destination, date)


@router.get("/detail/{departure_id}", response_model=DepartureDetail)
async def get_departure_detail(
    departure_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = DepartureService(db)
    return await svc.get_detail(departure_id)


@router.get("/", response_model=DepartureListResponse)
async def list_agency_departures(
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = DepartureService(db)
    departures = await svc.list_by_agency(current_user.agency_id)
    return {"items": departures, "total": len(departures)}


@router.patch("/{departure_id}/status", response_model=DeparturePublic)
async def update_departure_status(
    departure_id: int,
    data: DepartureStatusUpdate,
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = DepartureService(db)
    return await svc.update_status(departure_id, current_user.agency_id, data.status)
