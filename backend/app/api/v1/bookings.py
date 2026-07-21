from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.booking import (
    BookingAssignWasher,
    BookingCancel,
    BookingCreate,
    BookingReschedule,
    BookingResponse,
    BookingTrackingResponse,
)
from app.services.booking_service import BookingService


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    return service.create_booking(
        customer=current_user,
        data=booking,
    )


@router.get(
    "/my-bookings",
    response_model=list[BookingResponse],
)
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    return service.get_customer_bookings(
        current_user.id,
    )


@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
def get_booking(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    return service.get_booking(
        booking_id,
        current_user,
    )


@router.get(
    "/{booking_id}/tracking",
    response_model=BookingTrackingResponse,
)
def get_booking_tracking(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    return service.get_booking_tracking(
        booking_id,
        current_user,
    )


@router.patch(
    "/{booking_id}/cancel",
    response_model=BookingResponse,
)
def cancel_booking(
    booking_id: UUID,
    data: BookingCancel,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    return service.cancel_booking(
        booking_id=booking_id,
        current_user=current_user,
        reason=data.reason,
    )


@router.patch(
    "/{booking_id}/reschedule",
    response_model=BookingResponse,
)
def reschedule_booking(
    booking_id: UUID,
    data: BookingReschedule,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    return service.reschedule_booking(
        booking_id=booking_id,
        current_user=current_user,
        data=data,
    )


@router.patch(
    "/{booking_id}/assign-washer",
    response_model=BookingResponse,
)
def assign_washer(
    booking_id: UUID,
    data: BookingAssignWasher,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    return service.assign_washer(
        booking_id=booking_id,
        washer_id=data.washer_id,
        current_user=current_user,
    )

@router.patch(
    "/{booking_id}/auto-assign",
    response_model=BookingResponse,
)
def auto_assign(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.auto_assign_washer(
        booking_id,
        current_user,
    )