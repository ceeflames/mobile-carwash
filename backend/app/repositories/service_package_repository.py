from uuid import UUID

from sqlalchemy.orm import Session

from app.models.service_package import ServicePackage


class ServicePackageRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        service_package: ServicePackage,
    ):
        self.db.add(service_package)
        self.db.commit()
        self.db.refresh(service_package)

        return service_package

    def get_all(self):
        return (
            self.db.query(ServicePackage)
            .order_by(ServicePackage.name)
            .all()
        )

    def get_active(self):
        return (
            self.db.query(ServicePackage)
            .filter(ServicePackage.is_active == True)
            .order_by(ServicePackage.name)
            .all()
        )

    def get_by_id(
        self,
        package_id: UUID,
    ):
        return (
            self.db.query(ServicePackage)
            .filter(ServicePackage.id == package_id)
            .first()
        )

    def get_by_name(
        self,
        name: str,
    ):
        return (
            self.db.query(ServicePackage)
            .filter(ServicePackage.name == name)
            .first()
        )

    def save(
        self,
        service_package: ServicePackage,
    ):
        self.db.commit()
        self.db.refresh(service_package)

        return service_package

    def delete(
        self,
        service_package: ServicePackage,
    ):
        self.db.delete(service_package)
        self.db.commit()