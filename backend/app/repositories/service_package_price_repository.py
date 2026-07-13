from uuid import UUID

from sqlalchemy.orm import Session

from app.models.enums import VehicleType
from app.models.service_package_price import (
    ServicePackagePrice,
)


class ServicePackagePriceRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        price: ServicePackagePrice,
    ):
        self.db.add(price)
        self.db.commit()
        self.db.refresh(price)

        return price
    def get_all(self):
        return (
        self.db.query(ServicePackagePrice)
        .all()
    )

    def get_by_package(
        self,
        package_id: UUID,
    ):
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
    ):
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
    ):
        return (
            self.db.query(ServicePackagePrice)
            .filter(ServicePackagePrice.id == price_id)
            .first()
        )

    def save(
        self,
        price: ServicePackagePrice,
    ):
        self.db.commit()
        self.db.refresh(price)

        return price

    def delete(
        self,
        price: ServicePackagePrice,
    ):
        self.db.delete(price)
        self.db.commit()