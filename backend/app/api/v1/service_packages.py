from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.service_package import (
    ServicePackageResponse,
)
from app.services.service_package_service import (
    ServicePackageService,
)

router = APIRouter(
    prefix="/service-packages",
    tags=["Service Packages"],
)


@router.get(
    "",
    response_model=list[ServicePackageResponse],
)
def get_packages(
    db: Session = Depends(get_db),
):

    service = ServicePackageService(db)

    return service.get_public_packages()


@router.get(
    "/{package_id}",
    response_model=ServicePackageResponse,
)
def get_package(
    package_id: UUID,
    db: Session = Depends(get_db),
):

    service = ServicePackageService(db)

    return service.get_by_id(package_id)