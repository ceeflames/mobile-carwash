from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleResponse,
    VehicleUpdate,
)
from app.services.vehicle_service import VehicleService

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"],
)

@router.post(
    "",
    response_model=VehicleResponse,
)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = VehicleService(db)

    try:
        return service.create(
            current_user,
            vehicle,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
@router.get(
    "",
    response_model=list[VehicleResponse],
)
    
def get_my_vehicles(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

        service = VehicleService(db)

        return service.get_my_vehicles(current_user)

@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse,
)
def update_vehicle(
    vehicle_id: UUID,
    vehicle: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = VehicleService(db)

    try:
        return service.update(
            vehicle_id,
            current_user,
            vehicle,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
@router.delete("    /{vehicle_id}")
def delete_vehicle(
    vehicle_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = VehicleService(db)

    try:
        service.delete(
            vehicle_id,
            current_user,
        )

        return {"detail": "Vehicle deleted successfully."}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )