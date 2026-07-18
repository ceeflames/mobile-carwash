from fastapi import (
    APIRouter,
    Depends,
    Header,
    Request,
)
import hashlib
import hmac
from app.core.config import settings

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.payment import (
    PaymentInitialize,
    PaymentResponse,
    PaymentInitializationResponse
)
from app.exceptions.custom_exceptions import (
    BadRequestException,
)

from app.services.payment_service import PaymentService

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "/initialize",
    response_model=PaymentInitializationResponse,
)
def initialize_payment(
    data: PaymentInitialize,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PaymentService(db)

    return service.initialize_payment(
        booking_id=data.booking_id,
        customer=current_user,
        provider=data.provider,
    )


@router.get(
    "/history",
    response_model=list[PaymentResponse],
)
def payment_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PaymentService(db)

    return service.payment_history(
        current_user,
    )


@router.get(
    "/{reference}",
    response_model=PaymentInitializationResponse,
)
def verify_payment(
    reference: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = PaymentService(db)

    return service.verify_payment(
        reference,
    )

@router.post(
    "/webhook",
    status_code=200,
)
async def paystack_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_paystack_signature: str | None = Header(default=None),
):

    body = await request.body()

    expected_signature = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode(),
        body,
        hashlib.sha512,
    ).hexdigest()

    if (
        x_paystack_signature is None
        or x_paystack_signature != expected_signature
    ):
        raise BadRequestException(
            "Invalid Paystack signature."
        )

    payload = await request.json()

    event = payload.get("event")

    if event != "charge.success":
        return {
            "message": "Event ignored."
        }

    reference = payload["data"]["reference"]

    service = PaymentService(db)

    service.verify_payment(
        reference,
    )

    return {
        "message": "Webhook processed."
    }