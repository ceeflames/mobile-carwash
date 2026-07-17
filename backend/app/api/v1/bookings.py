from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
    BookingReschedule,
    BookingCancel,
    BookingAssignWasher,
)

from app.services.booking_service import BookingService

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.post(
    "",
    response_model=BookingResponse,
)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.create_booking(
        current_user,
        booking,
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
        booking_id,
        current_user,
        data,
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
        booking_id,
        current_user,
        data.reason,
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
        booking_id,
        data.washer_id,
        current_user,
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
        booking_id,
        data.washer_id,
        data.dispatcher_id,
        current_user,
    )