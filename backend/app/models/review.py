from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel


class Review(BaseModel):
    __tablename__ = "reviews"

    booking_id: Mapped[str] = mapped_column(
        ForeignKey("bookings.id"),
        unique=True,
        nullable=False,
    )

    customer_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    washer_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    booking = relationship(
        "Booking",
        back_populates="review",
    )

    customer = relationship(
        "User",
        foreign_keys=[customer_id],
    )

    washer = relationship(
        "User",
        foreign_keys=[washer_id],
    )