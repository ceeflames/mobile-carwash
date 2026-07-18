from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.booking import BookingResponse

from app.services.booking_service import BookingService
from app.models.enums import BookingStatus

router = APIRouter(
    prefix="/washer",
    tags=["Washer"],
)


@router.get(
    "/bookings",
    response_model=list[BookingResponse],
)
def get_my_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.get_washer_bookings(
        current_user.id,
    )


@router.patch(
    "/bookings/{booking_id}/accept",
    response_model=BookingResponse,
)
def accept_booking(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.update_status(
        booking_id=booking_id,
        new_status=BookingStatus.ACCEPTED,
        current_user=current_user,
    )


@router.patch(
    "/bookings/{booking_id}/en-route",
    response_model=BookingResponse,
)
def en_route(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.update_status(
        booking_id=booking_id,
        new_status=BookingStatus.EN_ROUTE,
        current_user=current_user,
    )

@router.patch(
    "/bookings/{booking_id}/arrived",
    response_model=BookingResponse,
)
def arrived(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.update_status(
        booking_id=booking_id,
        new_status=BookingStatus.ARRIVED,
        current_user=current_user,
    )


@router.patch(
    "/bookings/{booking_id}/start",
    response_model=BookingResponse,
)
def start_wash(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.update_status(
        booking_id=booking_id,
        new_status=BookingStatus.IN_PROGRESS,
        current_user=current_user,
    )


@router.patch(
    "/bookings/{booking_id}/complete",
    response_model=BookingResponse,
)
def complete_wash(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = BookingService(db)

    return service.update_status(
        booking_id=booking_id,
        new_status=BookingStatus.COMPLETED,
        current_user=current_user,
    )