from uuid import UUID

from sqlalchemy.orm import Session

from app.core.logger import setup_logger
from app.exceptions.custom_exceptions import (
    ForbiddenException,
    NotFoundException,
)
from app.models.address import Address
from app.models.user import User
from app.repositories.address_repository import AddressRepository
from app.schemas.address import (
    AddressCreate,
    AddressUpdate,
)

logger = setup_logger(__name__)


class AddressService:

    def __init__(self, db: Session):
        self.repository = AddressRepository(db)

    def create(
        self,
        owner: User,
        data: AddressCreate,
    ):

        logger.info(
            "Creating address for user %s",
            owner.email,
        )

        # Automatically make the first address the default
        is_default = data.is_default

        if self.repository.count_by_owner(owner.id) == 0:
            is_default = True

        # If this address should become default,
        # remove the default flag from the old one.
        if is_default:

            default_address = (
                self.repository.get_default_by_owner(
                    owner.id
                )
            )

            if default_address:
                default_address.is_default = False
                self.repository.save(default_address)

        address = Address(
            user_id=owner.id,
            title=data.title,
            street_address=data.street_address,
            city=data.city,
            state=data.state,
            landmark=data.landmark,
            additional_notes=data.additional_notes,
            latitude=data.latitude,
            longitude=data.longitude,
            is_default=is_default,
        )

        created = self.repository.create(address)

        self.repository.commit()
        self.repository.refresh(created)

        logger.info(
            "Address %s created.",
            created.id,
        )

        return created

    def get_my_addresses(
        self,
        owner: User,
    ):

        logger.info(
            "Fetching addresses for %s",
            owner.email,
        )

        return self.repository.get_by_owner(owner.id)

    def update(
        self,
        address_id: UUID,
        owner: User,
        data: AddressUpdate,
    ):

        address = self.repository.get_by_id(address_id)

        if address is None:
            raise NotFoundException(
                "Address not found."
            )

        if address.user_id != owner.id:
            raise ForbiddenException(
                "You cannot edit this address."
            )

        updates = data.model_dump(
            exclude_unset=True
        )

        # If making this the default,
        # remove default from previous one.
        if updates.get("is_default"):

            default_address = (
                self.repository.get_default_by_owner(
                    owner.id
                )
            )

            if (
                default_address
                and default_address.id != address.id
            ):
                default_address.is_default = False
                self.repository.save(default_address)

        for key, value in updates.items():
            setattr(address, key, value)

        updated = self.repository.save(address)

        logger.info(
            "Address %s updated.",
            address.id,
        )

        return updated

    def delete(
        self,
        address_id: UUID,
        owner: User,
    ):

        address = self.repository.get_by_id(address_id)

        if address is None:
            raise NotFoundException(
            "Address not found."
        )

        if address.user_id != owner.id:
            raise ForbiddenException(
            "You cannot delete this address."
        )

        was_default = address.is_default

        self.repository.delete(address)

        if was_default:

            new_default = self.repository.get_first_by_owner(
            owner.id
        )

        if new_default:
            new_default.is_default = True
            self.repository.save(new_default)

            logger.info(
                "Address %s is now the default.",
                new_default.id,
            )

        logger.info(
            "Address %s deleted.",
            address_id,
        )