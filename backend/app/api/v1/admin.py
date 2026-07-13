from fastapi import APIRouter, Depends

from app.dependencies.roles import require_roles
from app.models.enums import UserRole

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/dashboard")
def dashboard(
    user=Depends(
        require_roles(
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