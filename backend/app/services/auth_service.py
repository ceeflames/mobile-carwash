from sqlalchemy.orm import Session
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.exceptions.custom_exceptions import (
    ConflictException,
    UnauthorizedException,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserLogin, UserRegister


class AuthService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def register(self, data: UserRegister):

        existing_user = self.user_repository.get_by_email(
            data.email
        )

        if existing_user:
            raise ConflictException(
                "Email already registered."
            )
        existing_phone = self.user_repository.get_by_phone(
            data.phone
        )
        if existing_phone:
            raise ConflictException(
                "Phone number already registered."
            )
            

        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            password_hash=hash_password(data.password),
        )
        return self.user_repository.create(user)

    def login(self, data: UserLogin):

        user = self.user_repository.get_by_email(
            data.email
        )

        if not user:
            raise UnauthorizedException(
                "Invalid email or password."
            )

        if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise UnauthorizedException(
                "Invalid email or password."
            )

        token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role.value,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }