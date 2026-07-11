from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Enum,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel
from app.models.enums import VehicleType


class Vehicle(BaseModel):
    __tablename__ = "vehicles"

    owner_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    make: Mapped[str] = mapped_column(
        String(50)
    )

    model: Mapped[str] = mapped_column(
        String(50)
    )

    year: Mapped[int] = mapped_column(
        Integer
    )

    color: Mapped[str] = mapped_column(
        String(30)
    )

    plate_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        index=True,
    )

    vehicle_type: Mapped[VehicleType] = mapped_column(
        Enum(VehicleType)
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    owner = relationship(
        "User",
        back_populates="vehicles",
    )