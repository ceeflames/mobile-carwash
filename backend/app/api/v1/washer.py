from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.booking import BookingResponse
from app.services.booking_service import BookingService

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

    return service.accept_job(
        booking_id=booking_id,
        washer=current_user,
    )


@router.patch(
    "/bookings/{booking_id}/start-trip",
    response_model=BookingResponse,
)
def start_trip(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    return service.start_trip(
        booking_id,
        current_user,
    )


@router.patch(
    "/bookings/{booking_id}/arrive",
    response_model=BookingResponse,
)
def arrive(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    return service.arrive(
        booking_id,
        current_user,
    )


@router.patch(
    "/bookings/{booking_id}/start-washing",
    response_model=BookingResponse,
)
def start_washing(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    return service.start_washing(
        booking_id,
        current_user,
    )


@router.patch(
    "/bookings/{booking_id}/complete",
    response_model=BookingResponse,
)
def complete_job(
    booking_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    return service.complete_job(
        booking_id,
        current_user,
    )