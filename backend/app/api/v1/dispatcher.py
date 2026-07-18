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
    BookingAssignWasher,
    BookingResponse,
)

from app.services.booking_service import BookingService


router = APIRouter(
    prefix="/dispatcher",
    tags=["Dispatcher"],
)


@router.get(
    "/bookings/pending",
    response_model=list[BookingResponse],
)
def get_pending_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.get_pending_bookings(
        current_user,
    )


@router.get(
    "/bookings",
    response_model=list[BookingResponse],
)
def get_dispatcher_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.get_dispatcher_bookings(
        current_user,
    )


@router.patch(
    "/bookings/{booking_id}/assign",
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
        dispatcher_id=current_user.id,
        current_user=current_user,
    )

@router.patch(
    "/bookings/{booking_id}/reassign",
    response_model=BookingResponse,
)
def reassign_washer(
    booking_id: UUID,
    data: BookingAssignWasher,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.reassign_washer(
        booking_id=booking_id,
        washer_id=data.washer_id,
        dispatcher_id=current_user.id,
        current_user=current_user,
    )


@router.get(
    "/bookings/today",
    response_model=list[BookingResponse],
)
def get_today_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.get_today_bookings(
        current_user,
    )


@router.get(
    "/bookings/unassigned",
    response_model=list[BookingResponse],
)
def get_unassigned_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.get_unassigned_bookings(
        current_user,
    )


@router.get(
    "/dashboard")
def dispatcher_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.dispatcher_dashboard(
        current_user,
    )