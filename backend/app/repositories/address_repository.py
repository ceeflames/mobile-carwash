from uuid import UUID

from app.models.address import Address
from app.repositories.base_repository import BaseRepository


class AddressRepository(BaseRepository):

    def create(self, address):

        self.add(address)

        self.flush()

        self.refresh(address)

        return address

    def get_by_owner(
        self,
        owner_id: UUID,
    ) -> list[Address]:

        return (
            self.db.query(Address)
            .filter(
                Address.user_id == owner_id
            )
            .all()
        )

    def get_by_id(
        self,
        address_id: UUID,
    ) -> Address | None:

        return (
            self.db.query(Address)
            .filter(
                Address.id == address_id
            )
            .first()
        )

    def get_default_by_owner(
        self,
        owner_id: UUID,
    ) -> Address | None:

        return (
            self.db.query(Address)
            .filter(
                Address.user_id == owner_id,
                Address.is_default == True,
            )
            .first()
        )

    def count_by_owner(
        self,
        owner_id: UUID,
    ) -> int:

        return (
            self.db.query(Address)
            .filter(
                Address.user_id == owner_id
            )
            .count()
        )

    def get_first_by_owner(
        self,
        owner_id: UUID,
    ) -> Address | None:

        return (
            self.db.query(Address)
            .filter(
                Address.user_id == owner_id
            )
            .order_by(
                Address.created_at.asc()
            )
            .first()
        )

    def save(
        self,
        address: Address,
    ) -> Address:

        return address

    def remove(
        self,
        address: Address,
    ) -> None:

        self.delete(address)