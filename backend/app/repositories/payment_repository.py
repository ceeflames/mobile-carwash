from uuid import UUID

from sqlalchemy.orm import joinedload

from app.models.payment import Payment
from app.repositories.base_repository import BaseRepository


class PaymentRepository(BaseRepository):

    def create(
        self,
        payment: Payment,
    ) -> Payment:

        self.add(payment)
        self.flush()
        self.refresh(payment)

        return payment

    def get_by_id(
        self,
        payment_id: UUID,
    ) -> Payment | None:

        return (
            self.db.query(Payment)
            .options(
                joinedload(Payment.booking),
                joinedload(Payment.customer),
            )
            .filter(
                Payment.id == payment_id,
            )
            .first()
        )

    def get_by_booking(
        self,
        booking_id: UUID,
    ) -> Payment | None:

        return (
            self.db.query(Payment)
            .options(
                joinedload(Payment.booking),
                joinedload(Payment.customer),
            )
            .filter(
                Payment.booking_id == booking_id,
            )
            .first()
        )

    def get_by_reference(
        self,
        provider_reference: str,
    ) -> Payment | None:

        return (
            self.db.query(Payment)
            .options(
                joinedload(Payment.booking),
                joinedload(Payment.customer),
            )
            .filter(
                Payment.provider_reference
                == provider_reference,
            )
            .first()
        )

    def get_customer_payments(
        self,
        customer_id: UUID,
    ) -> list[Payment]:

        return (
            self.db.query(Payment)
            .options(
                joinedload(Payment.booking),
            )
            .filter(
                Payment.customer_id == customer_id,
            )
            .order_by(
                Payment.created_at.desc(),
            )
            .all()
        )

    def save(
        self,
        payment: Payment,
    ) -> Payment:

        self.flush()
        self.refresh(payment)

        return payment

    def remove(
        self,
        payment: Payment,
    ):

        self.delete(payment)