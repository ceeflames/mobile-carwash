from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel
from app.models.enums import (
    PaymentStatus,
    PaymentProvider,
)


class Payment(BaseModel):
    __tablename__ = "payments"

    booking_id: Mapped[str] = mapped_column(
        ForeignKey(
            "bookings.id",
            ondelete="CASCADE",
        ),
        unique=True,
    )

    customer_id: Mapped[str] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )

    provider: Mapped[PaymentProvider] = mapped_column(
        Enum(PaymentProvider),
    )

    provider_reference: Mapped[str] = mapped_column(
        String(255),
        unique=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="NGN",
    )

    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDING,
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    booking = relationship(
        "Booking",
        back_populates="payment",
    )

    customer = relationship(
        "User",
        back_populates="payments",
    )