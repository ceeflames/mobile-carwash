from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Mobile Car Wash API",
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health():
    return JSONResponse(
        {
            "status": "healthy",
            "service": settings.APP_NAME,
        }
    )