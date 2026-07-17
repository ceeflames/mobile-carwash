from uuid import UUID

from app.models.booking import Booking
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import joinedload

class BookingRepository(BaseRepository):

    def create(self,booking: Booking,) -> Booking:

        self.add(booking)
        self.flush()
        self.refresh(booking)
        return booking

    def get_by_id(
    self,
    booking_id: UUID,
    ) -> Booking | None:

        return (
        self.db.query(Booking)
        .options(
            joinedload(Booking.vehicle),
            joinedload(Booking.address),
            joinedload(Booking.service_package),
            joinedload(Booking.customer),
            joinedload(Booking.washer),
            joinedload(Booking.dispatcher),
        )
        .filter(Booking.id == booking_id)
        .first()
    )

    def get_by_reference(
        self,
        booking_reference: str,
    ) -> Booking | None:

        return (
            self.db.query(Booking)
            .filter(
                Booking.booking_reference == booking_reference
            )
            .first()
        )

    def get_customer_bookings(
    self,
    customer_id: UUID,
    ) -> list[Booking]:

        return (
        self.db.query(Booking)
        .options(
            joinedload(Booking.vehicle),
            joinedload(Booking.address),
            joinedload(Booking.service_package),
            joinedload(Booking.washer),
            joinedload(Booking.dispatcher),
        )
        .filter(
            Booking.customer_id == customer_id
        )
        .order_by(
            Booking.created_at.desc()
        )
        .all()
    )

    def get_all(self) -> list[Booking]:

        return (
        self.db.query(Booking)
        .options(
            joinedload(Booking.vehicle),
            joinedload(Booking.address),
            joinedload(Booking.service_package),
            joinedload(Booking.customer),
            joinedload(Booking.washer),
            joinedload(Booking.dispatcher),
        )
        .order_by(
            Booking.created_at.desc()
        )
        .all()
    )

    def save(
        self,
        booking: Booking,
    ) -> Booking:

        return booking

    def remove(
        self,
        booking: Booking,
    ):

        self.delete(booking)