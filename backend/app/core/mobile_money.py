"""
Mobile Money provider abstraction for Togo (Flooz / T-Money).

In production, swap SandboxProvider for PaygateProvider or CinetPayProvider.
The sandbox provider auto-initiates payments for development and testing.
"""

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from app.config import get_settings


class MoMoStatus(str, Enum):
    initiated = "initiated"
    pending = "pending"
    successful = "successful"
    failed = "failed"


@dataclass
class MoMoInitResult:
    provider_tx_id: str
    status: MoMoStatus
    message: str


@dataclass
class MoMoStatusResult:
    provider_tx_id: str
    status: MoMoStatus
    message: str


class MoMoProvider(ABC):
    """Abstract base for mobile money providers."""

    @abstractmethod
    async def initiate_payment(
        self,
        phone: str,
        amount: float,
        currency: str,
        reference: str,
    ) -> MoMoInitResult: ...

    @abstractmethod
    async def check_status(self, provider_tx_id: str) -> MoMoStatusResult: ...


class SandboxProvider(MoMoProvider):
    """Development/test provider. Immediately returns a successful initiation."""

    async def initiate_payment(
        self,
        phone: str,
        amount: float,
        currency: str,
        reference: str,
    ) -> MoMoInitResult:
        tx_id = f"SANDBOX-{uuid.uuid4().hex[:12].upper()}"
        return MoMoInitResult(
            provider_tx_id=tx_id,
            status=MoMoStatus.initiated,
            message=f"Payment request sent to {phone}",
        )

    async def check_status(self, provider_tx_id: str) -> MoMoStatusResult:
        return MoMoStatusResult(
            provider_tx_id=provider_tx_id,
            status=MoMoStatus.pending,
            message="Awaiting customer confirmation",
        )


class PaygateProvider(MoMoProvider):
    """Paygate Global provider for Togo (Flooz & T-Money)."""

    async def initiate_payment(
        self,
        phone: str,
        amount: float,
        currency: str,
        reference: str,
    ) -> MoMoInitResult:
        # TODO: Implement Paygate API integration
        raise NotImplementedError("Paygate integration not yet implemented")

    async def check_status(self, provider_tx_id: str) -> MoMoStatusResult:
        raise NotImplementedError("Paygate integration not yet implemented")


class CinetPayProvider(MoMoProvider):
    """CinetPay provider for West Africa (Flooz & T-Money)."""

    async def initiate_payment(
        self,
        phone: str,
        amount: float,
        currency: str,
        reference: str,
    ) -> MoMoInitResult:
        # TODO: Implement CinetPay API integration
        raise NotImplementedError("CinetPay integration not yet implemented")

    async def check_status(self, provider_tx_id: str) -> MoMoStatusResult:
        raise NotImplementedError("CinetPay integration not yet implemented")


def get_momo_provider() -> MoMoProvider:
    """Factory: returns the configured mobile money provider."""
    settings = get_settings()
    if settings.momo_provider == "paygate":
        return PaygateProvider()
    elif settings.momo_provider == "cinetpay":
        return CinetPayProvider()
    return SandboxProvider()
