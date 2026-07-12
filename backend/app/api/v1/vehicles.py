from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.schemas.response import ApiResponse
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
    response_model=ApiResponse[VehicleResponse],
)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = VehicleService(db)

    created_vehicle = service.create(
        current_user,
        vehicle,
    )

    return ApiResponse(
        success=True,
        message="Vehicle created successfully.",
        data=created_vehicle,
    )


@router.get(
    "",
    response_model=ApiResponse[list[VehicleResponse]],
)
def get_my_vehicles(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = VehicleService(db)

    vehicles = service.get_my_vehicles(current_user)

    return ApiResponse(
        success=True,
        message="Vehicles retrieved successfully.",
        data=vehicles,
    )


@router.put(
    "/{vehicle_id}",
    response_model=ApiResponse[VehicleResponse],
)
def update_vehicle(
    vehicle_id: UUID,
    vehicle: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = VehicleService(db)

    updated_vehicle = service.update(
        vehicle_id,
        current_user,
        vehicle,
    )

    return ApiResponse(
        success=True,
        message="Vehicle updated successfully.",
        data=updated_vehicle,
    )


@router.delete(
    "/{vehicle_id}",
    response_model=ApiResponse[None],
)
def delete_vehicle(
    vehicle_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = VehicleService(db)

    service.delete(
        vehicle_id,
        current_user,
    )

    return ApiResponse(
        success=True,
        message="Vehicle deleted successfully.",
        data=None,
    )