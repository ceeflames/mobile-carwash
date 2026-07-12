from sqlalchemy.orm import Session

from app.core.logger import setup_logger
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

logger = setup_logger(__name__)


class AuthService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def register(self, data: UserRegister):

        logger.info(
            "Registration attempt for %s",
            data.email,
        )

        existing_user = self.user_repository.get_by_email(
            data.email
        )

        if existing_user:
            logger.warning(
                "Duplicate email registration: %s",
                data.email,
            )
            raise ConflictException(
                "Email already registered."
            )

        existing_phone = self.user_repository.get_by_phone(
            data.phone
        )

        if existing_phone:
            logger.warning(
                "Duplicate phone registration: %s",
                data.phone,
            )
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

        created_user = self.user_repository.create(user)

        logger.info(
            "User registered successfully: %s",
            created_user.email,
        )

        return created_user

    def login(self, data: UserLogin):

        logger.info(
            "Login attempt for %s",
            data.email,
        )

        user = self.user_repository.get_by_email(
            data.email
        )

        if not user:
            logger.warning(
                "Failed login attempt: %s",
                data.email,
            )
            raise UnauthorizedException(
                "Invalid email or password."
            )

        if not verify_password(
            data.password,
            user.password_hash,
        ):
            logger.warning(
                "Invalid password for %s",
                data.email,
            )
            raise UnauthorizedException(
                "Invalid email or password."
            )

        token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role.value,
            }
        )

        logger.info(
            "User logged in successfully: %s",
            data.email,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }