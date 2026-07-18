from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import (
    PaymentProvider,
    PaymentStatus,
)


# -------------------------------------------------------
# Request Schemas
# -------------------------------------------------------

class PaymentInitialize(BaseModel):
    booking_id: UUID
    provider: PaymentProvider


# -------------------------------------------------------
# Response Schemas
# -------------------------------------------------------

class PaymentResponse(BaseModel):

    id: UUID

    booking_id: UUID

    customer_id: UUID

    provider: PaymentProvider

    provider_reference: str

    amount: Decimal

    currency: str

    status: PaymentStatus

    paid_at: datetime | None = None

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class PaymentHistoryResponse(PaymentResponse):
    pass


# -------------------------------------------------------
# Gateway Response
# -------------------------------------------------------

class PaymentInitializationResponse(BaseModel):

    payment: PaymentResponse

    checkout_url: str

    reference: str