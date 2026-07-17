from uuid import UUID

from app.models.service_package import ServicePackage
from app.repositories.base_repository import BaseRepository


class ServicePackageRepository(BaseRepository):

    def create(
        self,
        service_package: ServicePackage,
    ) -> ServicePackage:

        self.add(service_package)
        self.flush()
        self.refresh(service_package)

        return service_package

    def get_all(
        self,
    ) -> list[ServicePackage]:

        return (
            self.db.query(ServicePackage)
            .order_by(ServicePackage.name)
            .all()
        )

    def get_active(
        self,
    ) -> list[ServicePackage]:

        return (
            self.db.query(ServicePackage)
            .filter(
                ServicePackage.is_active == True
            )
            .order_by(ServicePackage.name)
            .all()
        )

    def get_by_id(
        self,
        package_id: UUID,
    ) -> ServicePackage | None:

        return (
            self.db.query(ServicePackage)
            .filter(
                ServicePackage.id == package_id
            )
            .first()
        )

    def get_by_name(
        self,
        name: str,
    ) -> ServicePackage | None:

        return (
            self.db.query(ServicePackage)
            .filter(
                ServicePackage.name == name
            )
            .first()
        )

    def save(
        self,
        service_package: ServicePackage,
    ) -> ServicePackage:

        self.commit()

        self.refresh(service_package)

        return service_package

    def remove(
        self,
        service_package: ServicePackage,
    ) -> None:

        self.delete(service_package)

        self.commit()