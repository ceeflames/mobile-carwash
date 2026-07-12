from uuid import UUID

from sqlalchemy.orm import Session

from app.models.address import Address


class AddressRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, address: Address) -> Address:
        self.db.add(address)
        self.db.commit()
        self.db.refresh(address)
        return address

    def get_by_owner(
        self,
        owner_id: UUID,
    ) -> list[Address]:
        return (
            self.db.query(Address)
            .filter(Address.user_id == owner_id)
            .all()
        )

    def get_by_id(
        self,
        address_id: UUID,
    ) -> Address | None:
        return (
            self.db.query(Address)
            .filter(Address.id == address_id)
            .first()
        )

    def save(
        self,
        address: Address,
    ) -> Address:
        self.db.commit()
        self.db.refresh(address)
        return address

    def delete(
        self,
        address: Address,
    ) -> None:
        self.db.delete(address)
        self.db.commit()

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
            .filter(Address.user_id == owner_id)
            .count()
        )
    
    def get_first_by_owner(
        self,
        owner_id: UUID,
    ) -> Address | None:
        return (
        self.db.query(Address)
        .filter(Address.user_id == owner_id)
        .order_by(Address.created_at.asc())
        .first()
    )