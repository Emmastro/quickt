from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user, require_agency_staff
from app.domains.auth.models import User
from app.domains.tickets.schemas import (
    BookingResponse,
    TicketCancelRequest,
    TicketCreateRequest,
    TicketDetail,
    TicketListResponse,
    TicketPublic,
)
from app.domains.tickets.service import TicketService

router = APIRouter()


@router.post("/", response_model=BookingResponse, status_code=201)
async def reserve_tickets(
    data: TicketCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = TicketService(db)
    booking_ref, tickets = await svc.reserve(
        customer_id=current_user.id,
        departure_id=data.departure_id,
        seats=[s.model_dump() for s in data.seats],
    )
    total = sum(t.price for t in tickets)
    return {"booking_reference": booking_ref, "tickets": tickets, "total": total}


@router.get("/my", response_model=TicketListResponse)
async def get_my_tickets(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = TicketService(db)
    tickets = await svc.get_customer_tickets(current_user.id)
    return {"items": tickets, "total": len(tickets)}


@router.get("/{ticket_id}", response_model=TicketDetail)
async def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = TicketService(db)
    return await svc.get_ticket_detail(ticket_id, current_user.id)


@router.get("/code/{code}", response_model=TicketPublic)
async def get_ticket_by_code(
    code: str,
    db: AsyncSession = Depends(get_db),
):
    svc = TicketService(db)
    return await svc.get_by_code(code)


@router.patch("/{ticket_id}/cancel", response_model=TicketPublic)
async def cancel_ticket(
    ticket_id: int,
    data: TicketCancelRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = TicketService(db)
    return await svc.cancel(ticket_id, current_user.id, data.reason)


@router.patch("/{ticket_id}/use", response_model=TicketPublic)
async def mark_ticket_used(
    ticket_id: int,
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = TicketService(db)
    return await svc.mark_used(ticket_id, current_user.agency_id)


@router.get("/departure/{departure_id}/passengers", response_model=TicketListResponse)
async def get_departure_passengers(
    departure_id: int,
    current_user: User = Depends(require_agency_staff),
    db: AsyncSession = Depends(get_db),
):
    svc = TicketService(db)
    tickets = await svc.get_departure_passengers(departure_id, current_user.agency_id)
    return {"items": tickets, "total": len(tickets)}
