from uuid import UUID

from sqlalchemy.orm import Session

from app.core.logger import setup_logger
from app.exceptions.custom_exceptions import (
    ForbiddenException,
    NotFoundException,
)
from app.models.user import User
from app.models.vehicle import Vehicle
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
)


logger = setup_logger(__name__)


class VehicleService:

    def __init__(self, db: Session):
        self.repository = VehicleRepository(db)

    def create(
        self,
        owner: User,
        data: VehicleCreate,
    ):

        logger.info(
            "Creating vehicle for user %s",
            owner.email,
        )

        vehicle = Vehicle(
            owner_id=owner.id,
            **data.model_dump(),
        )

        created_vehicle = self.repository.create(vehicle)

        logger.info(
            "Vehicle %s created successfully.",
            created_vehicle.id,
        )

        return created_vehicle

    def get_my_vehicles(
        self,
        owner: User,
    ):

        logger.info(
            "Retrieving vehicles for user %s",
            owner.email,
        )

        return self.repository.get_by_owner(owner.id)

    def update(
        self,
        vehicle_id: UUID,
        owner: User,
        data: VehicleUpdate,
    ):

        logger.info(
            "Updating vehicle %s",
            vehicle_id,
        )

        vehicle = self.repository.get_by_id(vehicle_id)

        if vehicle is None:

            logger.warning(
                "Vehicle %s not found.",
                vehicle_id,
            )

            raise NotFoundException(
                "Vehicle not found."
            )

        if vehicle.owner_id != owner.id:

            logger.warning(
                "User %s attempted to update vehicle %s they do not own.",
                owner.email,
                vehicle_id,
            )

            raise ForbiddenException(
                "You are not allowed to update this vehicle."
            )

        updates = data.model_dump(
            exclude_unset=True
        )

        for key, value in updates.items():
            setattr(vehicle, key, value)

        updated_vehicle = self.repository.save(vehicle)

        logger.info(
            "Vehicle %s updated successfully.",
            vehicle_id,
        )

        return updated_vehicle

    def delete(
        self,
        vehicle_id: UUID,
        owner: User,
    ):

        logger.info(
            "Deleting vehicle %s",
            vehicle_id,
        )

        vehicle = self.repository.get_by_id(vehicle_id)

        if vehicle is None:

            logger.warning(
                "Vehicle %s not found.",
                vehicle_id,
            )

            raise NotFoundException(
                "Vehicle not found."
            )

        if vehicle.owner_id != owner.id:

            logger.warning(
                "User %s attempted to delete vehicle %s they do not own.",
                owner.email,
                vehicle_id,
            )

            raise ForbiddenException(
                "You are not allowed to delete this vehicle."
            )

        self.repository.delete(vehicle)

        logger.info(
            "Vehicle %s deleted successfully.",
            vehicle_id,
        )