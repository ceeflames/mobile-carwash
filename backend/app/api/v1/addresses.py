from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.schemas.address import (
    AddressCreate,
    AddressResponse,
    AddressUpdate,
)
from app.services.address_service import AddressService

router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"],
)


@router.post(
    "",
    response_model=AddressResponse,
)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = AddressService(db)

    return service.create(
        current_user,
        address,
    )


@router.get(
    "",
    response_model=list[AddressResponse],
)
def get_my_addresses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = AddressService(db)

    return service.get_my_addresses(current_user)


@router.put(
    "/{address_id}",
    response_model=AddressResponse,
)
def update_address(
    address_id: UUID,
    address: AddressUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = AddressService(db)

    return service.update(
        address_id,
        current_user,
        address,
    )


@router.delete(
    "/{address_id}",
)
def delete_address(
    address_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = AddressService(db)

    service.delete(
        address_id,
        current_user,
    )

    return {
        "detail": "Address deleted successfully."
    }