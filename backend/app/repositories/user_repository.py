from sqlalchemy.orm import Session

from app.core.logger import setup_logger
from app.models.user import User

logger = setup_logger(__name__)


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        logger.info(
            "Looking up user by email: %s",
            email,
        )

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_by_phone(self, phone: str):
        logger.info(
            "Looking up user by phone: %s",
            phone,
        )

        return (
            self.db.query(User)
            .filter(User.phone == phone)
            .first()
        )

    def get_by_id(self, user_id):
        logger.info(
            "Looking up user by ID: %s",
            user_id,
        )

        return self.db.get(User, user_id)

    def create(self, user: User):
        logger.info(
            "Saving new user: %s",
            user.email,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        logger.info(
            "User created successfully. ID: %s",
            user.id,
        )

        return user