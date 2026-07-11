from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.enums import UserRole


class RoleChecker:

    def __init__(self, allowed_roles):

        self.allowed_roles = allowed_roles

    def __call__(self, user=Depends(get_current_user)):

        if user.role not in self.allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied.",
            )

        return user