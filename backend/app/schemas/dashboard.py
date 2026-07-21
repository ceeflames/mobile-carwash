from pydantic import BaseModel

from app.schemas.booking import BookingResponse
from app.schemas.staff import StaffResponse


class DispatcherDashboardResponse(BaseModel):

    pending_bookings: int

    assigned_bookings: int

    washing_bookings: int

    completed_bookings: int

    available_washers: int

    busy_washers: int

    offline_washers: int

    recent_bookings: list[BookingResponse]

    available_washers_list: list[StaffResponse]