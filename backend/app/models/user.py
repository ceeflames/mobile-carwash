from sqlalchemy import Boolean, Enum, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel
from app.models.enums import UserRole


class User(BaseModel):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(100))

    last_name: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(String(255))

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.CUSTOMER,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    phone_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    vehicles = relationship(
    "Vehicle",
    back_populates="owner",
    cascade="all, delete",
)