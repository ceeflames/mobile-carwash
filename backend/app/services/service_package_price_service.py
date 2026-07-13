from uuid import UUID

from app.models.service_package_price import ServicePackagePrice
from app.repositories.service_package_price_repository import (
    ServicePackagePriceRepository,
)
from app.schemas.service_package_price import (
    ServicePackagePriceCreate,
    ServicePackagePriceUpdate,
)


class ServicePackagePriceService:

    def __init__(self, db):
        self.repository = ServicePackagePriceRepository(db)

    def create(
        self,
        package_id: UUID,
        data: ServicePackagePriceCreate,
    ):

        existing = self.repository.get_by_package_and_vehicle(
            data.service_package_id,
            data.vehicle_type,
        )

        if existing:
            raise ValueError(
                "Price already exists for this vehicle type."
            )

        price = ServicePackagePrice(
            service_package_id=package_id,
            **data.model_dump(),
        )

        return self.repository.create(price)

    def get_all(self):
        return self.repository.get_all()

    def get_by_package(
        self,
        package_id: UUID,
    ):
        return self.repository.get_by_package(
            package_id,
        )

    def update(
        self,
        price_id: UUID,
        data: ServicePackagePriceUpdate,
    ):

        price = self.repository.get_by_id(price_id)

        if not price:
            raise ValueError(
                "Price not found."
            )

        updates = data.model_dump(
            exclude_unset=True,
        )

        for key, value in updates.items():
            setattr(price, key, value)

        return self.repository.save(price)

    def delete(
        self,
        price_id: UUID,
    ):

        price = self.repository.get_by_id(price_id)

        if not price:
            raise ValueError(
                "Price not found."
            )

        self.repository.delete(price)