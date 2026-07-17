from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import (
    BadRequestException,
    NotFoundException,
)

from app.models.service_package_price import ServicePackagePrice

from app.repositories.service_package_price_repository import (
    ServicePackagePriceRepository,
)

from app.repositories.service_package_repository import (
    ServicePackageRepository,
)

from app.schemas.service_package_price import (
    ServicePackagePriceCreate,
    ServicePackagePriceUpdate,
)


class ServicePackagePriceService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.price_repository = (
            ServicePackagePriceRepository(db)
        )

        self.package_repository = (
            ServicePackageRepository(db)
        )

    def create(
        self,
        data: ServicePackagePriceCreate,
    ) -> ServicePackagePrice:

        package = (
            self.package_repository.get_by_id(
                data.service_package_id
            )
        )

        if not package:
            raise NotFoundException(
                "Service package not found."
            )

        duplicate = (
            self.price_repository.get_duplicate(
                data.service_package_id,
                data.vehicle_type,
            )
        )

        if duplicate:
            raise BadRequestException(
                "Price already exists for this vehicle type."
            )

        price = ServicePackagePrice(
            service_package_id=data.service_package_id,
            vehicle_type=data.vehicle_type,
            price=data.price,
            is_active=True,
        )

        return self.price_repository.create(price)

    def get_by_package(
        self,
        package_id: UUID,
    ):

        return (
            self.price_repository.get_by_package(
                package_id
            )
        )

    def get_by_id(
        self,
        price_id: UUID,
    ):

        price = (
            self.price_repository.get_by_id(
                price_id
            )
        )

        if not price:
            raise NotFoundException(
                "Price not found."
            )

        return price

    def update(
        self,
        price_id: UUID,
        data: ServicePackagePriceUpdate,
    ):

        price = self.get_by_id(
            price_id
        )

        if data.vehicle_type is not None:

            duplicate = (
                self.price_repository.get_duplicate(
                    price.service_package_id,
                    data.vehicle_type,
                )
            )

            if (
                duplicate
                and duplicate.id != price.id
            ):
                raise BadRequestException(
                    "Vehicle type already has a price."
                )

            price.vehicle_type = (
                data.vehicle_type
            )

        if data.price is not None:
            price.price = data.price

        if data.is_active is not None:
            price.is_active = data.is_active

        return self.price_repository.save(
            price
        )

    def delete(
        self,
        price_id: UUID,
    ):

        price = self.get_by_id(
            price_id
        )

        self.price_repository.remove(
            price
        )