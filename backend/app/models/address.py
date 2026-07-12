from sqlalchemy import (
    Boolean,
    ForeignKey,
    Float,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel


class Address(BaseModel):
    __tablename__ = "addresses"

    user_id: Mapped[str] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )

    title: Mapped[str] = mapped_column(
        String(100)
    )

    street_address: Mapped[str] = mapped_column(
        String(255)
    )

    city: Mapped[str] = mapped_column(
        String(100)
    )

    state: Mapped[str] = mapped_column(
        String(100)
    )

    landmark: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    additional_notes: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    user = relationship(
        "User",
        back_populates="addresses",
    )