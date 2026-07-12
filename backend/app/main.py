from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.core.config import settings
from app.api.v1.admin import router as admin_router
from app.api.v1.vehicles import router as vehicles_router
from app.exceptions.handlers import (
    register_exception_handlers,
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
from app.middleware.logging import log_requests
from app.api.v1.addresses import (
    router as addresses_router,
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(vehicles_router)
register_exception_handlers(app)
app.middleware("http")(log_requests)
app.include_router(addresses_router)


@app.get("/")
def root():
    return {
        "message": "Mobile Car Wash API is running."
    }