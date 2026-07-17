from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.dependencies.auth import get_current_user

from app.exceptions.custom_exceptions import (
    UnauthorizedException,
)

from app.models.enums import UserRole
from app.models.user import User

from app.schemas.service_package_price import (
    ServicePackagePriceCreate,
    ServicePackagePriceResponse,
    ServicePackagePriceUpdate,
)

from app.services.service_package_price_service import (
    ServicePackagePriceService,
)

router = APIRouter(
    prefix="/service-package-prices",
    tags=["Service Package Prices"],
)


def require_admin(
    current_user: User,
):

    if current_user.role not in (
        UserRole.ADMIN,
        UserRole.SUPER_ADMIN,
    ):
        raise UnauthorizedException(
            "Admin access required."
        )


@router.post(
    "",
    response_model=ServicePackagePriceResponse,
)
def create_price(
    data: ServicePackagePriceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    require_admin(current_user)

    service = ServicePackagePriceService(db)

    return service.create(data)


@router.get(
    "/package/{package_id}",
    response_model=list[ServicePackagePriceResponse],
)
def get_package_prices(
    package_id: UUID,
    db: Session = Depends(get_db),
):

    service = ServicePackagePriceService(db)

    return service.get_by_package(
        package_id
    )


@router.get(
    "/{price_id}",
    response_model=ServicePackagePriceResponse,
)
def get_price(
    price_id: UUID,
    db: Session = Depends(get_db),
):

    service = ServicePackagePriceService(db)

    return service.get_by_id(
        price_id
    )


@router.patch(
    "/{price_id}",
    response_model=ServicePackagePriceResponse,
)
def update_price(
    price_id: UUID,
    data: ServicePackagePriceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    require_admin(current_user)

    service = ServicePackagePriceService(db)

    return service.update(
        price_id,
        data,
    )


@router.delete(
    "/{price_id}",
)
def delete_price(
    price_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    require_admin(current_user)

    service = ServicePackagePriceService(db)

    service.delete(
        price_id
    )

    return {
        "message": "Price deleted successfully."
    }