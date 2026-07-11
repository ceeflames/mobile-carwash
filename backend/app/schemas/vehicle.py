from uuid import UUID

from pydantic import BaseModel

from app.models.enums import VehicleType


class VehicleCreate(BaseModel):
    make: str
    model: str
    year: int
    color: str
    plate_number: str
    vehicle_type: VehicleType
    is_default: bool = False


class VehicleUpdate(BaseModel):
    make: str | None = None
    model: str | None = None
    year: int | None = None
    color: str | None = None
    plate_number: str | None = None
    vehicle_type: VehicleType | None = None
    is_default: bool | None = None


class VehicleResponse(BaseModel):
    id: UUID
    make: str
    model: str
    year: int
    color: str
    plate_number: str
    vehicle_type: VehicleType
    is_default: bool

    model_config = {
        "from_attributes": True
    }