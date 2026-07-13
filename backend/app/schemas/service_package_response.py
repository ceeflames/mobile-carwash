from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import VehicleType


class ServicePackagePriceResponse(BaseModel):
    id: UUID
    vehicle_type: VehicleType
    price: Decimal
    is_active: bool

    model_config = {
        "from_attributes": True,
    }


class ServicePackageResponse(BaseModel):
    id: UUID
    name: str
    description: str
    estimated_duration: int
    is_active: bool

    prices: list[ServicePackagePriceResponse] = []

    model_config = {
        "from_attributes": True,
    }