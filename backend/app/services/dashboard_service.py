from sqlalchemy.orm import Session

from app.models.enums import (
    BookingStatus,
    UserRole,
)
from app.repositories.booking_repository import BookingRepository
from app.repositories.user_repository import UserRepository
from app.schemas.dashboard import DispatcherDashboardResponse
from app.exceptions.custom_exceptions import ForbiddenException


class DashboardService:

    def __init__(self, db: Session):

        self.db = db

        self.booking_repository = BookingRepository(db)

        self.user_repository = UserRepository(db)

    def get_dispatcher_dashboard(
        self,
        current_user,
    ) -> DispatcherDashboardResponse:

        if current_user.role not in (
            UserRole.DISPATCHER,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        ):
            raise ForbiddenException(
                "Dispatcher access required."
            )

        return DispatcherDashboardResponse(

            pending_bookings=self.booking_repository.count_by_status(
                BookingStatus.PENDING,
            ),

            assigned_bookings=self.booking_repository.count_by_status(
                BookingStatus.ASSIGNED,
            ),

            washing_bookings=self.booking_repository.count_by_status(
                BookingStatus.WASHING,
            ),

            completed_bookings=self.booking_repository.count_by_status(
                BookingStatus.COMPLETED,
            ),

            available_washers=self.user_repository.count_available_washers(),

            busy_washers=self.user_repository.count_busy_washers(),

            offline_washers=self.user_repository.count_offline_washers(),

            recent_bookings=self.booking_repository.get_recent_bookings(),

            available_washers_list=self.user_repository.get_available_washers(),
        )