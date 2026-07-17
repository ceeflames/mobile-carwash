from uuid import UUID

from app.models.booking_status_history import (
    BookingStatusHistory,
)
from app.repositories.base_repository import (
    BaseRepository,
)


class BookingStatusHistoryRepository(
    BaseRepository,
):

    def create(
        self,
        history: BookingStatusHistory,
    ) -> BookingStatusHistory:

        self.add(history)
        self.flush()
        self.refresh(history)

        return history

    def get_booking_history(
        self,
        booking_id: UUID,
    ) -> list[BookingStatusHistory]:

        return (
            self.db.query(
                BookingStatusHistory
            )
            .filter(
                BookingStatusHistory.booking_id == booking_id
            )
            .order_by(
                BookingStatusHistory.created_at.asc()
            )
            .all()
        )