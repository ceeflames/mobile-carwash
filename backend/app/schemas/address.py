from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AddressCreate(BaseModel):
    title: str
    street_address: str
    city: str
    state: str
    landmark: str | None = None
    additional_notes: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_default: bool = False


class AddressUpdate(BaseModel):
    title: str | None = None
    street_address: str | None = None
    city: str | None = None
    state: str | None = None
    landmark: str | None = None
    additional_notes: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_default: bool | None = None


class AddressResponse(BaseModel):
    id: UUID
    title: str
    street_address: str
    city: str
    state: str
    landmark: str | None
    additional_notes: str | None
    latitude: float | None
    longitude: float | None
    is_default: bool

    model_config = ConfigDict(
        from_attributes=True
    )