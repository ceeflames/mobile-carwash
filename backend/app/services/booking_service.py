from decimal import Decimal
from uuid import uuid4
from uuid import UUID
from datetime import datetime, timezone
from app.models import booking
from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import (
    BadRequestException,
    NotFoundException,
    ForbiddenException,
)

from app.models.booking import Booking
from app.models.booking_status_history import (
    BookingStatusHistory,
)
from app.models.enums import (
    BookingStatus,
    PaymentStatus,
    WasherAvailability,
)

from app.models.user import User, UserRole

from app.repositories.address_repository import (
    AddressRepository,
)
from app.repositories.booking_repository import (
    BookingRepository,
)
from app.repositories.booking_status_history_repository import (
    BookingStatusHistoryRepository,
)
from app.repositories.service_package_price_repository import (
    ServicePackagePriceRepository,
)
from app.repositories.service_package_repository import (
    ServicePackageRepository,
)
from app.repositories.vehicle_repository import (
    VehicleRepository,
)

from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
    BookingTrackingResponse,
    BookingReschedule
)
from app.repositories.user_repository import UserRepository

from app.repositories.booking_status_history_repository import (
    BookingStatusHistoryRepository,
)
class BookingService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.booking_repository = BookingRepository(db)

        self.booking_status_history_repository = (
            BookingStatusHistoryRepository(db)      
        )
        self.history_repository = (
            BookingStatusHistoryRepository(db)
        )

        self.vehicle_repository = (
            VehicleRepository(db)
        )

        self.address_repository = (
            AddressRepository(db)
        )

        self.service_package_repository = (
            ServicePackageRepository(db)
        )

        self.price_repository = (
            ServicePackagePriceRepository(db)
        )
        self.user_repository = (
            UserRepository(db)
        )

    def _generate_booking_reference(
        self,
        ) -> str:

            while True:

                reference = (
                    f"MCW-{uuid4().hex[:8].upper()}"
                )

                existing = (
                    self.booking_repository
                    .get_by_reference(reference)
                )

                if not existing:
                    return reference
                

    def _validate_vehicle(
                self,
                vehicle_id,
                customer_id,
            ):
                vehicle = (
                    self.vehicle_repository
                    .get_by_id(vehicle_id)
                )

                if not vehicle:
                    raise NotFoundException(
                        "Vehicle not found."
                    )

                if vehicle.owner_id != customer_id:

                    raise BadRequestException(
                        "Vehicle does not belong to you."
                    )

                return vehicle
        
    def _validate_address(
        self,
        address_id,
        customer_id,
    ):

        address = (
            self.address_repository
            .get_by_id(address_id)
        )

        if not address:

            raise NotFoundException(
                "Address not found."
            )

        if address.user_id != customer_id:

            raise BadRequestException(
                "Address does not belong to you."
            )

        return address
    
    def _validate_service_package(
        self,
        package_id,
    ):

        package = (
            self.service_package_repository
            .get_by_id(package_id)
        )

        if not package:

            raise NotFoundException(
                "Service package not found."
            )

        if not package.is_active:

            raise BadRequestException(
                "Service package is inactive."
            )

        return package
    def _get_package_price(
        self,
        package_id,
        vehicle_type,
        ) -> Decimal:

        package_price = (
            self.price_repository
            .get_by_package_and_vehicle(
                package_id,
                vehicle_type,
            )
        )

        if not package_price:
            raise BadRequestException(
                "No pricing found for this vehicle type."
            )

        return package_price.price
    
    def _create_status_history(
        self,
        booking_id,
        from_status,
        to_status,
        changed_by_id,
        reason=None,
        old_scheduled_at=None,
        new_scheduled_at=None,
    ):

        history = BookingStatusHistory(
            booking_id=booking_id,
            from_status=from_status,
            to_status=to_status,
            changed_by_id=changed_by_id,
            reason=reason,
            old_scheduled_at=old_scheduled_at,
            new_scheduled_at=new_scheduled_at,
        )

        self.history_repository.create(history)

    def _change_status(
        self,
        booking: Booking,
        changed_by: User,
        new_status: BookingStatus,
    ):

        old_status = booking.status

        booking.status = new_status

        self.booking_repository.save(
            booking,
        )

        self._create_status_history(
            booking_id=booking.id,
            changed_by_id=changed_by.id,
            from_status=old_status,
            to_status=new_status,
        )

        self.db.commit()

        self.db.refresh(booking)

        return self.booking_repository.get_by_id(
            booking.id,
        )
    
    def create_booking(
        self,
        customer: User,
        data: BookingCreate,
    ) -> Booking:

        try:

            vehicle = self._validate_vehicle(
                data.vehicle_id,
                customer.id,
            )

            self._validate_address(
                data.address_id,
                customer.id,
            )

            self._validate_service_package(
                data.service_package_id,
            )

            final_price = self._get_package_price(
                data.service_package_id,
                vehicle.vehicle_type,
            )

            booking = Booking(

                booking_reference=
                self._generate_booking_reference(),

                customer_id=customer.id,

                vehicle_id=data.vehicle_id,

                address_id=data.address_id,

                service_package_id=data.service_package_id,

                scheduled_at=data.scheduled_at,

                final_price=final_price,

                customer_note=data.customer_note,

                status=BookingStatus.PENDING,

                payment_status=PaymentStatus.PENDING,
            )

            self.booking_repository.create(
                booking
            )

            self.db.flush()

            self._create_status_history(
                booking_id=booking.id,
                changed_by_id=customer.id,
                from_status=None,
                to_status=BookingStatus.PENDING,
            )

            self.db.commit()

            return self.booking_repository.get_by_id(
                booking.id
            )

        except Exception:

            self.db.rollback()

            raise

    def get_customer_bookings(
    self,
    customer_id,):

        return (
        self.booking_repository
        .get_customer_bookings(customer_id)
    )

    def get_booking(
    self,
    booking_id,
    current_user: User,):
        booking = (
            self.booking_repository
            .get_by_id(booking_id)
        )

        if not booking:
            raise NotFoundException(
                "Booking not found."
            )

        if (
            booking.customer_id != current_user.id
            and current_user.role.value
            not in (
                "admin",
                "super_admin",
                "dispatcher",
            )
        ):
            raise BadRequestException(
                "You cannot access this booking."
            )

        return booking
    
    def cancel_booking(
        self,
        booking_id,
        current_user: User,
        reason: str,
    ):
        booking = self.get_booking(
        booking_id,
        current_user,
    )
        
        if booking.status not in (
        BookingStatus.PENDING,
        BookingStatus.ASSIGNED,):
            raise BadRequestException(
            "Booking cannot be cancelled."
        )
        booking.cancelled_reason = reason

        self._change_status(
            booking,
            BookingStatus.CANCELLED,
            current_user.id,
            reason,
        )
        self.db.commit()

        return booking
    
    def reschedule_booking(
        self,
        booking_id,
        current_user: User,
        data,
    ):

        booking = self.get_booking(
            booking_id,
            current_user,
        )

        if booking.status not in (
            BookingStatus.PENDING,
            BookingStatus.ASSIGNED,
        ):
            raise BadRequestException(
                "Booking cannot be rescheduled."
            )

        old_schedule = booking.scheduled_at

        booking.scheduled_at = data.scheduled_at
        self.booking_repository.save(booking)
        self.db.flush()

        self._create_status_history(
            booking_id=booking.id,
            changed_by_id=current_user.id,
            from_status=booking.status,
            to_status=booking.status,
            reason=data.reason,
            old_scheduled_at=old_schedule,
            new_scheduled_at=data.scheduled_at,
        )

        self.db.commit()

        self.db.refresh(booking)

        return booking
    
    def assign_washer(
        self,
        booking_id,
        washer_id,
        current_user: User,
    ):

        booking = self.get_booking(
            booking_id,
            current_user,
        )

        if booking.status != BookingStatus.PENDING:
            raise BadRequestException(
                "Washer can only be assigned to pending bookings."
            )

        if booking.washer_id:
            raise BadRequestException(
                "Booking already has a washer."
            )

        washer = self.user_repository.get_washer_by_id(
            washer_id
        )

        if washer is None:
            raise NotFoundException(
                "Washer not found."
            )

        booking.washer_id = washer.id
        booking.dispatcher_id = current_user.id

        return self._change_status(
            booking,
            current_user,
            BookingStatus.ASSIGNED,
        )   

    
    def get_pending_bookings(
        self,
        current_user: User,
    ):

        self._ensure_dispatcher(current_user)

        return self.booking_repository.get_pending_bookings()


    def get_dispatcher_bookings(
        self,
        current_user: User,
    ):

        self._ensure_dispatcher(current_user)

        return self.booking_repository.get_dispatcher_bookings(
            current_user.id,
        )
    
    def _ensure_dispatcher(
        self,
        current_user: User,
    ):

        if current_user.role not in (
            UserRole.DISPATCHER,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        ):
            raise ForbiddenException(
                "Dispatcher access required."
            )


    def _ensure_washer(
        self,
        current_user: User,
    ):

        if current_user.role != UserRole.WASHER:
            raise ForbiddenException(
                "Washer access required."
            )
        
    def get_today_bookings(
        self,
        current_user: User,
    ):

        self._ensure_dispatcher(
            current_user,
        )

        return self.booking_repository.get_today_bookings()
    
    def get_unassigned_bookings(
        self,
        current_user: User,
    ):

        self._ensure_dispatcher(
            current_user,
        )

        return self.booking_repository.get_unassigned_bookings()
    
    def reassign_washer(
        self,
        booking_id: UUID,
        washer_id: UUID,
        dispatcher_id: UUID,
        current_user: User,
    ):

        self._ensure_dispatcher(current_user)

        booking = self.get_booking(
            booking_id,
            current_user,
        )

        washer = self.user_repository.get_washer_by_id(
            washer_id,
        )

        if washer is None:
            raise NotFoundException(
                "Washer not found."
            )

        booking.washer_id = washer.id

        booking.dispatcher_id = dispatcher_id

        return self._change_status(
                    booking,
                    current_user,
                    BookingStatus.ASSIGNED,
                )

    def dispatcher_dashboard(
        self,
        current_user: User,
    ):

        self._ensure_dispatcher(
            current_user,
        )

        pending = self.booking_repository.get_pending_bookings()

        assigned = self.booking_repository.get_dispatcher_bookings(
            current_user.id,
        )

        today = self.booking_repository.get_today_bookings()

        unassigned = (
            self.booking_repository.get_unassigned_bookings()
        )

        return {
            "pending_bookings": len(pending),
            "assigned_bookings": len(assigned),
            "today_bookings": len(today),
            "unassigned_bookings": len(unassigned),
        }
    def update_status(
        self,
        booking_id: UUID,
        new_status: BookingStatus,
        current_user: User,
    ):

        self._ensure_washer(current_user)

        booking = self.booking_repository.get_by_id(
            booking_id,
        )

        if booking is None:
            raise NotFoundException(
                "Booking not found."
            )

        if booking.washer_id != current_user.id:
            raise ForbiddenException(
                "This booking is not assigned to you."
            )

        old_status = booking.status

        valid_transitions = {
            BookingStatus.ASSIGNED: BookingStatus.ACCEPTED,
            BookingStatus.ACCEPTED: BookingStatus.ON_THE_WAY,
            BookingStatus.ON_THE_WAY: BookingStatus.ARRIVED,
            BookingStatus.ARRIVED: BookingStatus.WASHING,
            BookingStatus.WASHING: BookingStatus.COMPLETED,
        }

        expected_status = valid_transitions.get(old_status)

        if expected_status != new_status:
            raise BadRequestException(
                f"Invalid status transition from "
                f"{old_status.value} to {new_status.value}."
            )

        booking.status = new_status

        self.booking_repository.save(
            booking,
        )

        self._create_status_history(
            booking_id=booking.id,
            changed_by_id=current_user.id,
            from_status=old_status,
            to_status=new_status,
        )

        self.db.commit()

        return self.booking_repository.get_by_id(
            booking.id,
        )
    
    def accept_job(
        self,
        booking_id: UUID,
        washer: User,
    ) -> Booking:

        booking = self.booking_repository.get_by_id(
            booking_id,
        )

        if booking is None:
            raise NotFoundException(
                "Booking not found."
            )

        if booking.washer_id != washer.id:
            raise BadRequestException(
                "This booking is not assigned to you."
            )

        if booking.status != BookingStatus.ASSIGNED:
            raise BadRequestException(
                "Booking cannot be accepted."
            )

        return self._change_status(
            booking,
            washer,
            BookingStatus.ACCEPTED,
        )
    
    def start_trip(
        self,
        booking_id: UUID,
        washer: User,
    ) -> Booking:

        booking = self.booking_repository.get_by_id(
            booking_id,
        )

        if booking is None:
            raise NotFoundException(
                "Booking not found."
            )

        if booking.washer_id != washer.id:
            raise BadRequestException(
                "This booking is not assigned to you."
            )

        if booking.status != BookingStatus.ACCEPTED:
            raise BadRequestException(
                "Booking is not ready."
            )

        return self._change_status(
            booking,
            washer,
            BookingStatus.ON_THE_WAY,
        )
    
    def arrive(
        self,
        booking_id: UUID,
        washer: User,
    ) -> Booking:

        booking = self.booking_repository.get_by_id(
            booking_id,
        )

        if booking is None:
            raise NotFoundException(
                "Booking not found."
            )

        if booking.washer_id != washer.id:
            raise BadRequestException(
                "This booking is not assigned to you."
            )

        if booking.status != BookingStatus.ON_THE_WAY:
            raise BadRequestException(
                "Booking is not on the way."
            )

        return self._change_status(
            booking,
            washer,
            BookingStatus.ARRIVED,
        )
    
    def start_washing(
        self,
        booking_id: UUID,
        washer: User,
    ) -> Booking:

        booking = self.booking_repository.get_by_id(
            booking_id,
        )

        if booking is None:
            raise NotFoundException(
                "Booking not found."
            )

        if booking.washer_id != washer.id:
            raise BadRequestException(
                "This booking is not assigned to you."
            )

        if booking.status != BookingStatus.ARRIVED:
            raise BadRequestException(
                "Booking has not arrived."
            )

        return self._change_status(
            booking,
            washer,
            BookingStatus.WASHING,
        )
    def complete_job(
        self,
        booking_id: UUID,
        washer: User,
    ) -> Booking:

        booking = self.booking_repository.get_by_id(
            booking_id,
        )

        if booking is None:
            raise NotFoundException(
                "Booking not found."
            )

        if booking.washer_id != washer.id:
            raise BadRequestException(
                "This booking is not assigned to you."
            )

        if booking.status != BookingStatus.WASHING:
            raise BadRequestException(
                "Booking is not being washed."
            )

        return self._change_status(
            booking,
            washer,
            BookingStatus.COMPLETED,
        )
    
    def get_booking_tracking(
        self,
        booking_id: UUID,
        current_user: User,
    ) -> BookingTrackingResponse:

        booking = self.get_booking(
            booking_id,
            current_user,
        )

        history = (
            self.booking_status_history_repository
            .get_booking_history(
                booking.id,
            )
        )

        return {
            "booking": booking,
            "timeline": history,
        }
    
    def auto_assign_washer(
        self,
        booking_id: UUID,
        dispatcher: User,
    ):
            
        booking = self.get_booking(
            booking_id,
            dispatcher,
        )
        if booking.washer_id:
            raise BadRequestException(
                "Booking already has a washer."
            )

        if booking.status != BookingStatus.PENDING:
            raise BadRequestException(
                "Booking cannot be assigned."
            )

        washers = self.user_repository.get_available_washers()
      

        if not washers:
            raise BadRequestException(
                "No available washers."
            )
        
        washer = washers[0]

        booking.washer_id = washer.id
        booking.dispatcher_id = dispatcher.id

        washer.availability = WasherAvailability.BUSY

        return self._change_status(
            booking,
            dispatcher,
            BookingStatus.ASSIGNED,
        )