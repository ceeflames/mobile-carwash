from uuid import UUID

from pydantic import BaseModel

from app.schemas.service_package_price import (
    ServicePackagePriceResponse,
)


class ServicePackageCreate(BaseModel):
    name: str
    description: str
    estimated_duration: int


class ServicePackageUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    estimated_duration: int | None = None
    is_active: bool | None = None


class ServicePackageResponse(BaseModel):
    id: UUID
    name: str
    description: str
    estimated_duration: int
    is_active: bool

    # Nested prices for each vehicle type
    prices: list[ServicePackagePriceResponse] = []

    model_config = {
        "from_attributes": True,
    }