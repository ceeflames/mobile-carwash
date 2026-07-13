from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    Numeric,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel
from app.models.enums import VehicleType


class ServicePackagePrice(BaseModel):
    __tablename__ = "service_package_prices"

    __table_args__ = (
        UniqueConstraint(
            "service_package_id",
            "vehicle_type",
            name="uq_service_package_vehicle",
        ),
    )

    service_package_id: Mapped[str] = mapped_column(
        ForeignKey(
            "service_packages.id",
            ondelete="CASCADE",
        )
    )

    vehicle_type: Mapped[VehicleType] = mapped_column(
        Enum(VehicleType)
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    service_package = relationship(
        "ServicePackage",
        back_populates="prices",
    )