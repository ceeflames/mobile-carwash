from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.exceptions.custom_exceptions import (
    BadRequestException,
)

from app.models.user import User

from app.models.enums import UserRole

from app.repositories.user_repository import UserRepository

from app.schemas.staff import StaffCreate


class StaffService:

    def __init__(self, db: Session):

        self.db = db

        self.user_repository = UserRepository(db)

    def create_staff(
        self,
        data: StaffCreate,
    ):

        existing_email = (
            self.user_repository.get_by_email(
                data.email
            )
        )

        if existing_email:
            raise BadRequestException(
                "Email already exists."
            )

        existing_phone = (
            self.user_repository.get_by_phone(
                data.phone
            )
        )

        if existing_phone:
            raise BadRequestException(
                "Phone already exists."
            )

        staff = User(

            first_name=data.first_name,

            last_name=data.last_name,

            email=data.email,

            phone=data.phone,

            password_hash=hash_password(
                data.password
            ),

            role=data.role,

            is_active=True,
        )

        created = self.user_repository.create(
            staff
        )

        return created
    
    def get_all_staff(self):
        return self.user_repository.get_staff()
    
    def get_washers(self):
        return self.user_repository.get_by_role(
            UserRole.WASHER
        )
    
    def get_dispatchers(self):
        return self.user_repository.get_by_role(
            UserRole.DISPATCHER
        )