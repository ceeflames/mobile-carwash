from sqlalchemy import (
    Boolean,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel


class ServicePackage(BaseModel):
    __tablename__ = "service_packages"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
    )

    estimated_duration: Mapped[int] = mapped_column(
        Integer,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    prices = relationship(
        "ServicePackagePrice",
        back_populates="service_package",
        cascade="all, delete-orphan",
    )