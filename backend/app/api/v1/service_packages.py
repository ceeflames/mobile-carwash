from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.dependencies.auth import get_current_user

from app.exceptions.custom_exceptions import (
    UnauthorizedException,
)

from app.models.enums import UserRole
from app.models.user import User

from app.schemas.service_package import (
    ServicePackageCreate,
    ServicePackageResponse,
    ServicePackageUpdate,
)

from app.services.service_package_service import (
    ServicePackageService,
)

router = APIRouter(
    prefix="/service-packages",
    tags=["Service Packages"],
)
def require_admin(
    current_user: User,
):

    if current_user.role not in (
        UserRole.ADMIN,
        UserRole.SUPER_ADMIN,
    ):

        raise UnauthorizedException(
            "Admin access required."
        )
    
@router.post(
    "",
    response_model=ServicePackageResponse,
)
def create_service_package(
    data: ServicePackageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    require_admin(current_user)

    service = ServicePackageService(db)

    return service.create(data)

@router.get(
    "",
    response_model=list[ServicePackageResponse],
)
def get_service_packages(
    db: Session = Depends(get_db),
):

    service = ServicePackageService(db)

    return service.get_all()

@router.get(
    "/active",
    response_model=list[ServicePackageResponse],
)
def get_active_packages(
    db: Session = Depends(get_db),
):

    service = ServicePackageService(db)

    return service.get_active()

@router.get(
    "/{package_id}",
    response_model=ServicePackageResponse,
)
def get_service_package(
    package_id: UUID,
    db: Session = Depends(get_db),
):

    service = ServicePackageService(db)

    return service.get_by_id(
        package_id
    )

@router.patch(
    "/{package_id}",
    response_model=ServicePackageResponse,
)
def update_service_package(
    package_id: UUID,
    data: ServicePackageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    require_admin(current_user)

    service = ServicePackageService(db)

    return service.update(
        package_id,
        data,
    )

@router.delete(
    "/{package_id}",
)
def delete_service_package(
    package_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    require_admin(current_user)

    service = ServicePackageService(db)

    service.delete(package_id)

    return {
        "message": "Service package deleted successfully."
    }

