from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel
from app.models.enums import BookingStatus


class BookingStatusHistory(BaseModel):
    __tablename__ = "booking_status_history"

    booking_id: Mapped[str] = mapped_column(
        ForeignKey(
            "bookings.id",
            ondelete="CASCADE",
        )
    )

    from_status: Mapped[BookingStatus | None] = mapped_column(
        Enum(BookingStatus),
        nullable=True,
    )

    to_status: Mapped[BookingStatus | None] = mapped_column(
        Enum(BookingStatus),
        nullable=True,
    )

    changed_by_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # NEW
    old_scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # NEW
    new_scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    booking = relationship(
        "Booking",
        back_populates="status_history",
    )

    changed_by = relationship(
        "User",
        back_populates="status_changes",
    )