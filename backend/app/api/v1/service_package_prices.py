from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.roles import require_admin
from app.schemas.service_package_price import (
    ServicePackagePriceCreate,
    ServicePackagePriceUpdate,
    ServicePackagePriceResponse,
)
from app.services.service_package_price_service import (
    ServicePackagePriceService,
)

router = APIRouter(
    prefix="/admin/service-packages/{package_id}/prices",
    tags=["Admin - Service Package Prices"],
    dependencies=[Depends(require_admin)],
)

@router.post(
    "",
    response_model=ServicePackagePriceResponse,
)
def create_price(
    package_id: UUID,
    data: ServicePackagePriceCreate,
    db: Session = Depends(get_db),
):

    service = ServicePackagePriceService(db)

    data = data.model_copy(
        update={
            "service_package_id": package_id,
        }
    )

    return service.create(data)