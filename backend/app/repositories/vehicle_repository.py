from uuid import UUID

from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle


class VehicleRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, vehicle: Vehicle) -> Vehicle:
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def get_by_owner(self, owner_id: UUID) -> list[Vehicle]:
        return (
            self.db.query(Vehicle)
            .filter(Vehicle.owner_id == owner_id)
            .all()
        )

    def get_by_id(
        self,
        vehicle_id: UUID,
    ) -> Vehicle | None:
        return (
            self.db.query(Vehicle)
            .filter(Vehicle.id == vehicle_id)
            .first()
        )

    def save(self, vehicle: Vehicle) -> Vehicle:
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def delete(self, vehicle: Vehicle) -> None:
        self.db.delete(vehicle)
        self.db.commit()