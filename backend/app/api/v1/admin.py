from fastapi import APIRouter, Depends

from app.dependencies.roles import RoleChecker
from app.models.enums import UserRole

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/dashboard")
def dashboard(
    user=Depends(
        RoleChecker(
            [
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN,
            ]
        )
    ),
):

    return {
        "message": "Welcome Admin",
        "user": user.email,
    }