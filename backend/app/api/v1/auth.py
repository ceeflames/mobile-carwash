from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.schemas.auth import (
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.schemas.response import ApiResponse
from app.schemas.token import Token
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=ApiResponse[UserResponse],
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    created_user = service.register(user)

    return ApiResponse(
        success=True,
        message="User registered successfully.",
        data=created_user,
    )


@router.post(
    "/login",
    response_model=ApiResponse[Token],
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    token = service.login(credentials)

    return ApiResponse(
        success=True,
        message="Login successful.",
        data=token,
    )


@router.get(
    "/me",
    response_model=ApiResponse[UserResponse],
)
def me(
    current_user=Depends(get_current_user),
):
    return ApiResponse(
        success=True,
        message="Current user retrieved successfully.",
        data=current_user,
    )