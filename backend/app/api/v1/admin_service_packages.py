from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.roles import require_roles
from app.models.enums import UserRole
from app.schemas.service_package import (
    ServicePackageCreate,
    ServicePackageUpdate,
    ServicePackageResponse,
)
from app.services.service_package_service import (
    ServicePackageService,
)

router = APIRouter(
    prefix="/admin/service-packages",
    tags=["Admin - Service Packages"],
    dependencies=[Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        ))],
)
@router.post(
    "",
    response_model=ServicePackageResponse,
)
def create_package(
    data: ServicePackageCreate,
    db: Session = Depends(get_db),
):
    return ServicePackageService(db).create(data)

@router.get(
    "",
    response_model=list[ServicePackageResponse],
)
def get_all_packages(
    db: Session = Depends(get_db),
):
    return ServicePackageService(db).get_all_for_admin()

@router.put(
    "/{package_id}",
    response_model=ServicePackageResponse,
)
def update_package(
    package_id: UUID,
    data: ServicePackageUpdate,
    db: Session = Depends(get_db),
):
    return ServicePackageService(db).update(
        package_id,
        data,
    )
@router.delete("/{package_id}")
def delete_package(
    package_id: UUID,
    db: Session = Depends(get_db),
):

    ServicePackageService(db).delete(
        package_id,
    )

    return {
        "message": "Service package deleted successfully."
    }