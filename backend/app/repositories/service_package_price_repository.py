from uuid import UUID

from app.models.enums import VehicleType
from app.models.service_package_price import (
    ServicePackagePrice,
)
from app.repositories.base_repository import BaseRepository


class ServicePackagePriceRepository(BaseRepository):

    def create(
        self,
        price: ServicePackagePrice,
    ) -> ServicePackagePrice:

        self.add(price)
        self.flush()
        self.refresh(price)

        return price

    def get_by_package(
        self,
        package_id: UUID,
    ) -> list[ServicePackagePrice]:

        return (
            self.db.query(ServicePackagePrice)
            .filter(
                ServicePackagePrice.service_package_id
                == package_id
            )
            .all()
        )

    def get_by_package_and_vehicle(
        self,
        package_id: UUID,
        vehicle_type: VehicleType,
    ) -> ServicePackagePrice | None:

        return (
            self.db.query(ServicePackagePrice)
            .filter(
                ServicePackagePrice.service_package_id
                == package_id,
                ServicePackagePrice.vehicle_type
                == vehicle_type,
            )
            .first()
        )

    def get_by_id(
        self,
        price_id: UUID,
    ) -> ServicePackagePrice | None:

        return (
            self.db.query(ServicePackagePrice)
            .filter(
                ServicePackagePrice.id == price_id
            )
            .first()
        )

    def save(
        self,
        price: ServicePackagePrice,
    ) -> ServicePackagePrice:

        return price

    def remove(
        self,
        price: ServicePackagePrice,
    ) -> None:

        self.delete(price)

    def get_duplicate(
        self,
        package_id: UUID,
        vehicle_type: VehicleType,
        ) -> ServicePackagePrice | None:

        return (
        self.db.query(ServicePackagePrice)
        .filter(
            ServicePackagePrice.service_package_id == package_id,
            ServicePackagePrice.vehicle_type == vehicle_type,
        )
        .first()
    )