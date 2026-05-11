from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, NotFoundError
from app.domains.payments.models import Payment, PaymentMethod, PaymentStatus
from app.domains.tickets.models import Ticket, TicketStatus
from app.domains.tickets.service import TicketService


class PaymentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def initiate(
        self,
        booking_reference: str,
        method: str,
        phone: str,
    ) -> Payment:
        # Look up tickets for this booking
        result = await self.db.execute(
            select(Ticket).where(
                Ticket.booking_reference == booking_reference,
                Ticket.status == TicketStatus.reserved,
            )
        )
        tickets = list(result.scalars().all())
        if not tickets:
            raise NotFoundError("No reserved tickets found for this booking reference")

        # Calculate total
        total = sum(t.price for t in tickets)

        try:
            payment_method = PaymentMethod(method)
        except ValueError:
            raise BadRequestError(f"Invalid payment method: {method}")

        # Check if payment already exists
        existing = await self.db.execute(
            select(Payment).where(
                Payment.booking_reference == booking_reference,
                Payment.status == PaymentStatus.pending,
            )
        )
        if existing.scalar_one_or_none():
            raise BadRequestError("A pending payment already exists for this booking")

        # Create payment record
        payment = Payment(
            booking_reference=booking_reference,
            amount=total,
            method=payment_method,
            phone=phone,
            status=PaymentStatus.pending,
            provider_tx_id=f"SIM-{uuid.uuid4().hex[:12].upper()}",
        )
        self.db.add(payment)
        await self.db.flush()
        await self.db.refresh(payment)

        # In sandbox mode, auto-confirm the payment
        await self._auto_confirm(payment)

        return payment

    async def _auto_confirm(self, payment: Payment) -> None:
        """In sandbox mode, instantly confirm payment and tickets."""
        payment.status = PaymentStatus.confirmed
        payment.confirmed_at = datetime.now(timezone.utc)
        payment.provider_status = "sandbox_confirmed"

        # Confirm all tickets in this booking
        ticket_svc = TicketService(self.db)
        await ticket_svc.confirm_tickets(payment.booking_reference)

        await self.db.flush()
        await self.db.refresh(payment)

    async def handle_webhook(self, tx_id: str, status: str, reference: str) -> Payment:
        """Handle payment webhook (idempotent)."""
        result = await self.db.execute(
            select(Payment).where(Payment.provider_tx_id == tx_id)
        )
        payment = result.scalar_one_or_none()
        if not payment:
            raise NotFoundError("Payment not found")

        # Idempotent: don't process if already finalized
        if payment.status in (PaymentStatus.confirmed, PaymentStatus.failed):
            return payment

        if status == "success":
            payment.status = PaymentStatus.confirmed
            payment.confirmed_at = datetime.now(timezone.utc)
            payment.provider_status = status

            ticket_svc = TicketService(self.db)
            await ticket_svc.confirm_tickets(payment.booking_reference)
        else:
            payment.status = PaymentStatus.failed
            payment.provider_status = status

        await self.db.flush()
        await self.db.refresh(payment)
        return payment

    async def get_status(self, payment_id: int) -> Payment:
        result = await self.db.execute(
            select(Payment).where(Payment.id == payment_id)
        )
        payment = result.scalar_one_or_none()
        if not payment:
            raise NotFoundError("Payment not found")
        return payment

    async def get_customer_payments(self, customer_id: uuid.UUID) -> list[Payment]:
        # Get booking references for the customer's tickets
        ticket_result = await self.db.execute(
            select(Ticket.booking_reference)
            .where(Ticket.customer_id == customer_id)
            .distinct()
        )
        refs = [r[0] for r in ticket_result.all()]
        if not refs:
            return []

        result = await self.db.execute(
            select(Payment)
            .where(Payment.booking_reference.in_(refs))
            .order_by(Payment.created_at.desc())
        )
        return list(result.scalars().all())
