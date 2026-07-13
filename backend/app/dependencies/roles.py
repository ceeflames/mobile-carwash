from fastapi import Depends

from app.dependencies.auth import get_current_user
from app.exceptions.custom_exceptions import ForbiddenException
from app.models.enums import UserRole
from app.models.user import User


def require_roles(*allowed_roles: UserRole):
    """
    Restrict an endpoint to one or more user roles.
    """

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role not in allowed_roles:
            raise ForbiddenException(
                "You do not have permission to access this resource."
            )

        return current_user

    return role_checker