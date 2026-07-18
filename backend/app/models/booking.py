from decimal import Decimal

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel
from app.models.enums import (
    BookingStatus,
    PaymentStatus,
)


class Booking(BaseModel):
    __tablename__ = "bookings"

    booking_reference: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        index=True,
    )

    customer_id: Mapped[str] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )

    vehicle_id: Mapped[str] = mapped_column(
        ForeignKey(
            "vehicles.id",
            ondelete="CASCADE",
        )
    )

    address_id: Mapped[str] = mapped_column(
        ForeignKey(
            "addresses.id",
            ondelete="CASCADE",
        )
    )

    service_package_id: Mapped[str] = mapped_column(
        ForeignKey(
            "service_packages.id",
            ondelete="RESTRICT",
        )
    )

    service_package_price_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "service_package_prices.id",
            ondelete="SET NULL",
        ),
        nullable=True,
)


    washer_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    dispatcher_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    scheduled_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
    )

    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus),
        default=BookingStatus.PENDING,
    )

    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDING,
    )

    final_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )

    customer_note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    cancelled_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    customer = relationship(
        "User",
        foreign_keys=[customer_id],
        back_populates="customer_bookings",
    )

    washer = relationship(
        "User",
        foreign_keys=[washer_id],
        back_populates="assigned_bookings",
    )

    dispatcher = relationship(
        "User",
        foreign_keys=[dispatcher_id],
        back_populates="dispatched_bookings",
    )

    vehicle = relationship(
        "Vehicle",
        back_populates="bookings",
    )

    address = relationship(
        "Address",
        back_populates="bookings",
    )

    service_package = relationship(
        "ServicePackage",
        back_populates="bookings",
    )

    status_history = relationship(
        "BookingStatusHistory",
        back_populates="booking",
        cascade="all, delete-orphan",
    )
    service_package_price = relationship(
        "ServicePackagePrice",
        back_populates="bookings",
    )
    payment = relationship(
        "Payment",
        back_populates="booking",
        uselist=False,
    )