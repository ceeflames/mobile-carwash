from uuid import uuid4, UUID
from decimal import Decimal
from datetime import datetime, timezone
from app.models import payment
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.models.enums import (
    PaymentProvider,
    PaymentStatus,
)

from app.repositories.payment_repository import PaymentRepository
from app.repositories.booking_repository import BookingRepository

from app.models.user import User

from app.exceptions.custom_exceptions import (
    NotFoundException,
    BadRequestException,
)
from app.integrations.paystack import PaystackService
from app.schemas.payment import PaymentInitializationResponse

class PaymentService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.payment_repository = PaymentRepository(db)

        self.booking_repository = BookingRepository(db)

        self.paystack = PaystackService()

    def initialize_payment(
        self,
        booking_id: UUID,
        customer: User,
        provider: PaymentProvider,
    ) -> PaymentInitializationResponse:

        booking = self.booking_repository.get_by_id(
            booking_id,
        )

        if booking is None:
            raise NotFoundException(
                "Booking not found."
            )

        if booking.customer_id != customer.id:
            raise BadRequestException(
                "This booking does not belong to you."
            )

        existing = self.payment_repository.get_by_booking(
            booking.id,
        )

        if existing:
            raise BadRequestException(
                "Payment already exists."
            )

        reference = self.generate_reference()

        amount_kobo = int(
            booking.final_price * 100
        )

        if provider == PaymentProvider.PAYSTACK:

            response = (
                self.paystack.initialize_transaction(
                    email=customer.email,
                    amount=amount_kobo,
                    reference=reference,
                )
            )

            checkout_url = response["data"][
                "authorization_url"
            ]

        else:

            raise BadRequestException(
                "Payment provider not supported."
            )

        payment = Payment(

            booking_id=booking.id,

            customer_id=customer.id,

            provider=provider,

            provider_reference=reference,

            amount=booking.final_price,

            currency="NGN",

            status=PaymentStatus.PENDING,
        )

        self.payment_repository.create(payment)

        self.db.commit()

        self.db.refresh(payment)
        return PaymentInitializationResponse(
            payment=payment,
            checkout_url=checkout_url,
            reference=reference,
        )

    def verify_payment(
        self,
        provider_reference: str,
    ) -> Payment:

        payment = self.payment_repository.get_by_reference(
            provider_reference,
        )

        if payment is None:
            raise NotFoundException(
                "Payment not found."
            )
        if payment.status == PaymentStatus.PAID:
            return payment

        response = self.paystack.verify_transaction(
            provider_reference,
        )

        data = response["data"]

        if data["status"] != "success":
            raise BadRequestException(
                "Payment not successful."
            )

        payment.status = PaymentStatus.PAID

        payment.paid_at = datetime.now(timezone.utc)

        booking = self.booking_repository.get_by_id(
            payment.booking_id,
        )

        booking.payment_status = PaymentStatus.PAID

        self.payment_repository.save(
            payment,
        )

        self.booking_repository.save(
            booking,
        )

        self.db.commit()

        return payment

    def payment_history(
        self,
        customer: User,
    ):

        return (
            self.payment_repository
            .get_customer_payments(
                customer.id,
            )
        )

    @staticmethod
    def generate_reference():

        return (
            "MCW-"
            + uuid4().hex.upper()[:16]
        )