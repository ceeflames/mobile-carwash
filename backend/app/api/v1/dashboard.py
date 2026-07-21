from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.dashboard import DispatcherDashboardResponse
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dispatcher",
    tags=["Dispatcher Dashboard"],
)


@router.get(
    "/dashboard",
    response_model=DispatcherDashboardResponse,
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = DashboardService(db)

    return service.get_dispatcher_dashboard(
        current_user,
    )