from uuid import UUID

from sqlalchemy.orm import Session

from app.core.logger import setup_logger
from app.exceptions.custom_exceptions import (
    ConflictException,
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

    logger = setup_logger(__name__)

    def __init__(self, db: Session):
        self.repository = ServicePackageRepository(db)

    def create(
        self,
        data: ServicePackageCreate,
    ):

        existing = self.repository.get_by_name(
            data.name
        )

        if existing:
            raise ConflictException(
                "Service package already exists."
            )

        package = ServicePackage(
            **data.model_dump(),
        )

        package = self.repository.create(package)

        self.logger.info(
            f"Created service package '{package.name}'."
        )

        return package

    def get_all_for_admin(self):
        """
        Returns every service package,
        including inactive ones.
        """
        return self.repository.get_all()

    def get_public_packages(self):
        """
        Returns only active packages
        visible to customers.
        """
        return self.repository.get_active()

    def get_by_id(
        self,
        package_id: UUID,
    ):

        package = self.repository.get_by_id(
            package_id
        )

        if package is None:
            raise NotFoundException(
                "Service package not found."
            )

        return package

    def update(
        self,
        package_id: UUID,
        data: ServicePackageUpdate,
    ):

        package = self.repository.get_by_id(
            package_id
        )

        if package is None:
            raise NotFoundException(
                "Service package not found."
            )

        updates = data.model_dump(
            exclude_unset=True
        )

        for key, value in updates.items():
            setattr(package, key, value)

        package = self.repository.save(package)

        self.logger.info(
            f"Updated service package '{package.name}'."
        )

        return package

    def delete(
        self,
        package_id: UUID,
    ):

        package = self.repository.get_by_id(
            package_id
        )

        if package is None:
            raise NotFoundException(
                "Service package not found."
            )

        self.repository.delete(package)

        self.logger.info(
            f"Deleted service package '{package.name}'."
        )