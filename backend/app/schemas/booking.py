from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import (
    BookingStatus,
    PaymentStatus,
    VehicleType,
)
from app.schemas.address import AddressResponse


class BookingCreate(BaseModel):
    vehicle_id: UUID
    address_id: UUID
    service_package_id: UUID
    scheduled_at: datetime
    customer_note: str | None = None


class BookingUpdate(BaseModel):
    scheduled_at: datetime | None = None
    customer_note: str | None = None


# -------------------------------------------------------
# Nested Response Objects
# -------------------------------------------------------

class BookingVehicleResponse(BaseModel):
    id: UUID
    plate_number: str
    vehicle_type: VehicleType

    model_config = {
        "from_attributes": True,
    }


class BookingAddressResponse(BaseModel):
    id: UUID
    title: str
    address: str

    model_config = {
        "from_attributes": True,
    }


class BookingServicePackageResponse(BaseModel):
    id: UUID
    name: str
    estimated_duration: int

    model_config = {
        "from_attributes": True,
    }


# -------------------------------------------------------
# Booking Response
# -------------------------------------------------------

class BookingResponse(BaseModel):
    id: UUID

    booking_reference: str

    vehicle: BookingVehicleResponse

    address: AddressResponse

    service_package: BookingServicePackageResponse

    washer_id: UUID | None = None

    dispatcher_id: UUID | None = None

    scheduled_at: datetime

    status: BookingStatus

    payment_status: PaymentStatus

    final_price: Decimal

    customer_note: str | None = None

    cancelled_reason: str | None = None

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }

class BookingCancel(BaseModel):
    reason: str

class BookingReschedule(BaseModel):
    scheduled_at: datetime
    reason: str | None = None

class BookingAssignWasher(BaseModel):
    washer_id: UUID

class BookingTimelineItem(BaseModel):
    from_status: BookingStatus | None
    to_status: BookingStatus
    reason: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

class BookingTrackingResponse(BaseModel):

    booking: BookingResponse

    timeline: list[BookingTimelineItem]