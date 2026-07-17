from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import (
    BadRequestException,
    NotFoundException,
)

from app.models.service_package import ServicePackage

from app.repositories.service_package_repository import (
    ServicePackageRepository,
)

from app.schemas.service_package import (
    ServicePackageCreate,
    ServicePackageUpdate,
)


class ServicePackageService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.repository = (
            ServicePackageRepository(db)
        )

    def create(
        self,
        data: ServicePackageCreate,
    ) -> ServicePackage:

        existing = self.repository.get_by_name(
            data.name
        )

        if existing:
            raise BadRequestException(
                "Service package already exists."
            )

        package = ServicePackage(
            name=data.name,
            description=data.description,
            estimated_duration=data.estimated_duration,
            is_active=True,
        )

        self.db.add(package)
        self.db.flush()

        from app.models.service_package_price import (
            ServicePackagePrice,
        )

        for item in data.prices:

            price = ServicePackagePrice(
                service_package_id=package.id,
                vehicle_type=item.vehicle_type,
                price=item.price,
                is_active=True,
            )

            self.db.add(price)

        self.db.commit()

        self.db.refresh(package)

        return package

    def get_all(self):

        return self.repository.get_all()

    def get_active(self):

        return self.repository.get_active()

    def get_by_id(
        self,
        package_id: UUID,
    ):

        package = (
            self.repository.get_by_id(
                package_id
            )
        )

        if not package:
            raise NotFoundException(
                "Service package not found."
            )

        return package

    def update(
        self,
        package_id: UUID,
        data: ServicePackageUpdate,
    ):

        package = self.get_by_id(
            package_id
        )

        if (
            data.name
            and data.name != package.name
        ):
            existing = (
                self.repository.get_by_name(
                    data.name
                )
            )

            if existing:
                raise BadRequestException(
                    "Service package already exists."
                )

            package.name = data.name

        if data.description is not None:
            package.description = (
                data.description
            )

        if (
            data.estimated_duration
            is not None
        ):
            package.estimated_duration = (
                data.estimated_duration
            )

        if data.is_active is not None:
            package.is_active = (
                data.is_active
            )

        return self.repository.save(
            package
        )

    def delete(
        self,
        package_id: UUID,
    ):

        package = self.get_by_id(
            package_id
        )

        self.repository.delete(
            package
        )