from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import require_admin

from .schemas import RouteCreate, RouteListResponse, RoutePublic, RouteUpdate
from .service import RouteService
from app.domains.auth.models import User

router = APIRouter()


@router.post("/", response_model=RoutePublic, status_code=201)
async def create_route(
    data: RouteCreate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    svc = RouteService(db)
    return await svc.create(data)


@router.get("/", response_model=RouteListResponse)
async def list_routes(
    origin: str | None = None,
    destination: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    svc = RouteService(db)
    items, total = await svc.list(origin=origin, destination=destination, skip=skip, limit=limit)
    return RouteListResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/popular", response_model=list[RoutePublic])
async def get_popular_routes(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    svc = RouteService(db)
    return await svc.get_popular(limit)


@router.get("/{route_id}", response_model=RoutePublic)
async def get_route(route_id: int, db: AsyncSession = Depends(get_db)):
    svc = RouteService(db)
    return await svc.get_by_id(route_id)


@router.patch("/{route_id}", response_model=RoutePublic)
async def update_route(
    route_id: int,
    data: RouteUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    svc = RouteService(db)
    return await svc.update(route_id, data)
