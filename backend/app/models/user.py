from sqlalchemy import Boolean, Enum, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel
from app.models.enums import UserRole, WasherAvailability


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

    availability: Mapped[WasherAvailability] = mapped_column(
    Enum(WasherAvailability),
    nullable=False,
    default=WasherAvailability.OFFLINE,
    server_default=WasherAvailability.OFFLINE.value,
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

    addresses = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    customer_bookings = relationship(
        "Booking",
        foreign_keys="Booking.customer_id",
        back_populates="customer",
    )

    assigned_bookings = relationship(
        "Booking",
        foreign_keys="Booking.washer_id",
        back_populates="washer",
    )

    dispatched_bookings = relationship(
        "Booking",
        foreign_keys="Booking.dispatcher_id",
        back_populates="dispatcher",
    )

    status_changes = relationship(
        "BookingStatusHistory",
        foreign_keys="BookingStatusHistory.changed_by_id",
    )
    payments = relationship(
        "Payment",
        back_populates="customer",
    )