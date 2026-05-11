from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.domains.auth.models import User
from app.domains.trips.schemas import TripCreate, TripDetail, TripPublic, TripUpdate
from app.domains.trips.service import TripService

router = APIRouter()


@router.post("/", response_model=TripPublic, status_code=201)
async def create_trip(
    data: TripCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = TripService(db)
    return await svc.create(current_user.id, data.model_dump())


@router.get("/", response_model=list[TripDetail])
async def list_trips(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = TripService(db)
    return await svc.list(current_user.id)


@router.patch("/{trip_id}", response_model=TripPublic)
async def update_trip(
    trip_id: int,
    data: TripUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = TripService(db)
    return await svc.update(trip_id, current_user.id, data.model_dump(exclude_unset=True))


@router.delete("/{trip_id}", status_code=204)
async def delete_trip(
    trip_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = TripService(db)
    await svc.delete(trip_id, current_user.id)
