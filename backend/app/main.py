from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.core.config import settings
from app.api.v1.admin import router as admin_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(auth_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "message": "Mobile Car Wash API is running."
    }