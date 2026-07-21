from uuid import UUID

from pydantic import BaseModel

from app.models.enums import UserRole, WasherAvailability


class StaffCreate(BaseModel):

    first_name: str

    last_name: str

    email: str

    phone: str

    password: str

    role: UserRole


class StaffResponse(BaseModel):

    id: UUID

    first_name: str

    last_name: str

    email: str

    phone: str

    role: UserRole

    is_active: bool

class Config:
        from_attributes = True

class WasherAvailabilityUpdate(BaseModel):
    availability: WasherAvailability    