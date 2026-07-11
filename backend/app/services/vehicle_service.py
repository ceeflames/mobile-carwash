from uuid import UUID

from app.models.user import User
from app.models.vehicle import Vehicle
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
)


class VehicleService:

    def __init__(self, db):
        self.repository = VehicleRepository(db)

    def create(
        self,
        owner: User,
        data: VehicleCreate,
    ):

        vehicle = Vehicle(
            owner_id=owner.id,
            **data.model_dump(),
        )

        return self.repository.create(vehicle)

    def get_my_vehicles(
        self,
        owner: User,
    ):
        return self.repository.get_by_owner(owner.id)

    def update(
        self,
        vehicle_id: UUID,
        owner: User,
        data: VehicleUpdate,
    ):

        vehicle = self.repository.get_by_id(vehicle_id)

        if vehicle is None:
            raise ValueError("Vehicle not found.")

        if vehicle.owner_id != owner.id:
            raise ValueError("Not authorized.")

        updates = data.model_dump(
            exclude_unset=True
        )

        for key, value in updates.items():
            setattr(vehicle, key, value)

        return self.repository.save(vehicle)

    def delete(
        self,
        vehicle_id: UUID,
        owner: User,
    ):

        vehicle = self.repository.get_by_id(vehicle_id)

        if vehicle is None:
            raise ValueError("Vehicle not found.")

        if vehicle.owner_id != owner.id:
            raise ValueError("Not authorized.")

        self.repository.delete(vehicle)