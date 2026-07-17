from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
)

from app.db.session import get_db

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User

from app.models.enums import UserRole

from app.schemas.staff import (
    StaffCreate,
    StaffResponse,
)

from app.services.staff_service import (
    StaffService,
)

from app.exceptions.custom_exceptions import (
    ForbiddenException,
)
router = APIRouter(
    prefix="/staff",
    tags=["Staff"],
)

def admin_required(
    current_user: User,
):

    if current_user.role not in (

        UserRole.ADMIN,

        UserRole.SUPER_ADMIN,
    ):

        raise ForbiddenException(
            "Admin access required."
        )
    
@router.post(
    "",
    response_model=StaffResponse,
)
def create_staff(

    data: StaffCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    ),
):

    admin_required(current_user)

    service = StaffService(db)

    return service.create_staff(data)

@router.get(
    "",
    response_model=list[StaffResponse],
)
def get_staff(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    ),
):

    admin_required(current_user)

    service = StaffService(db)

    return service.get_all_staff()

@router.get(
    "/washers",
    response_model=list[StaffResponse],
)
def get_washers(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    ),
):

    admin_required(current_user)

    service = StaffService(db)

    return service.get_washers()

@router.get(
    "/dispatchers",
    response_model=list[StaffResponse],
)
def get_dispatchers(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    ),
):

    admin_required(current_user)

    service = StaffService(db)

    return service.get_dispatchers()