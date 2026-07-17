from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import BookingStatus


class BookingStatusHistoryResponse(BaseModel):
    id: UUID

    booking_id: UUID

    status: BookingStatus

    changed_by_id: UUID | None = None

    change_reason: str | None = None

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }