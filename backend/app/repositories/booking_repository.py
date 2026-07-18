from uuid import UUID
from datetime import datetime, timezone
from app.models.booking import Booking
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import joinedload
from app.models.enums import (
    BookingStatus,)

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

    def get_pending_bookings(
        self,
    ) -> list[Booking]:

        return (
            self.db.query(Booking)
            .options(
                joinedload(Booking.vehicle),
                joinedload(Booking.address),
                joinedload(Booking.customer),
                joinedload(Booking.service_package),
            )
            .filter(
                Booking.status == BookingStatus.PENDING
            )
            .order_by(
                Booking.scheduled_at.asc()
            )
            .all()
        )
    
    def get_washer_bookings(
    self,
    washer_id: UUID,
    ) -> list[Booking]:

        return (
            self.db.query(Booking)
            .options(
                joinedload(Booking.vehicle),
                joinedload(Booking.address),
                joinedload(Booking.customer),
                joinedload(Booking.service_package),
            )
            .filter(
                Booking.washer_id == washer_id
            )
            .order_by(
                Booking.scheduled_at.asc()
            )
            .all()
        )
    
    def get_dispatcher_bookings(
    self,
    dispatcher_id: UUID,
    ) -> list[Booking]:

        return (
            self.db.query(Booking)
            .options(
                joinedload(Booking.vehicle),
                joinedload(Booking.address),
                joinedload(Booking.customer),
                joinedload(Booking.service_package),
                joinedload(Booking.washer),
            )
            .filter(
                Booking.dispatcher_id == dispatcher_id
            )
            .order_by(
                Booking.scheduled_at.asc()
            )
            .all()
        )
    def delete(
        self,
        booking: Booking,
    ):

        super().delete(booking)

    def get_today_bookings(
        self,
    ) -> list[Booking]:

        today = datetime.now(timezone.utc).date()

        return (
            self.db.query(Booking)
            .options(
                joinedload(Booking.vehicle),
                joinedload(Booking.address),
                joinedload(Booking.customer),
                joinedload(Booking.washer),
                joinedload(Booking.dispatcher),
                joinedload(Booking.service_package),
            )
            .filter(
                Booking.scheduled_at >= today,
            )
            .order_by(
                Booking.scheduled_at.asc(),
            )
            .all()
        )
    
    def get_unassigned_bookings(
        self,
    ) -> list[Booking]:

        return (
            self.db.query(Booking)
            .options(
                joinedload(Booking.vehicle),
                joinedload(Booking.address),
                joinedload(Booking.customer),
                joinedload(Booking.service_package),
            )
            .filter(
                Booking.washer_id.is_(None),
            )
            .order_by(
                Booking.created_at.desc(),
            )
            .all()
        )