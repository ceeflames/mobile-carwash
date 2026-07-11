from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
    UnauthorizedException,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(BadRequestException)
    async def bad_request_handler(
        request: Request,
        exc: BadRequestException,
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(NotFoundException)
    async def not_found_handler(
        request: Request,
        exc: NotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_handler(
        request: Request,
        exc: UnauthorizedException,
    ):
        return JSONResponse(
            status_code=401,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ConflictException)
    async def conflict_handler(
        request: Request,
        exc: ConflictException,
    ):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )