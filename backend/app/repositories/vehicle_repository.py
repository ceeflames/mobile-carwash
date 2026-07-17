from uuid import UUID

from app.models.vehicle import Vehicle
from app.repositories.base_repository import BaseRepository


class VehicleRepository(BaseRepository):

    def create(
        self,
        vehicle: Vehicle,
    ) -> Vehicle:

        self.add(vehicle)

        self.flush()

        self.refresh(vehicle)

        return vehicle

    def get_by_owner(
        self,
        owner_id: UUID,
    ) -> list[Vehicle]:

        return (
            self.db.query(Vehicle)
            .filter(
                Vehicle.owner_id == owner_id
            )
            .all()
        )

    def get_by_id(
        self,
        vehicle_id: UUID,
    ) -> Vehicle | None:

        return (
            self.db.query(Vehicle)
            .filter(
                Vehicle.id == vehicle_id
            )
            .first()
        )

    def save(
        self,
        vehicle: Vehicle,
    ) -> Vehicle:

        self.flush()

        self.refresh(vehicle)

        return vehicle

    def remove(
        self,
        vehicle: Vehicle,
    ) -> None:

        self.delete(vehicle)