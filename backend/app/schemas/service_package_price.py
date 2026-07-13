from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import VehicleType


class ServicePackagePriceCreate(BaseModel):
    vehicle_type: VehicleType
    price: Decimal


class ServicePackagePriceUpdate(BaseModel):
    vehicle_type: VehicleType | None = None
    price: Decimal | None = None
    is_active: bool | None = None


class ServicePackagePriceResponse(BaseModel):
    id: UUID
    service_package_id: UUID
    vehicle_type: VehicleType
    price: Decimal
    is_active: bool

    model_config = {
        "from_attributes": True,
    }