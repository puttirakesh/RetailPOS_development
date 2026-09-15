from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import check_db_connection
from app.core.logging import get_logger, setup_logging
from app.middleware.request_context import RequestContextMiddleware
from app.routers import (
    auth,
    brands,
    categories,
    cities,
    groups,
    marks,
    states,
    taxes,
    uoms,
)

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "startup app_name=%s version=%s environment=%s",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.ENVIRONMENT,
    )
    yield
    logger.info("shutdown")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID", "Accept"],
    expose_headers=["X-Request-ID", "X-Response-Time-Ms"],
)

app.add_middleware(RequestContextMiddleware)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(brands.router, prefix="/api/v1")
app.include_router(uoms.router, prefix="/api/v1")
app.include_router(marks.router, prefix="/api/v1")
app.include_router(taxes.router, prefix="/api/v1")

app.include_router(states.router, prefix="/api/v1")
app.include_router(cities.router, prefix="/api/v1")
app.include_router(groups.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")

@app.get("/health", tags=["Observability"])
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/ready", tags=["Observability"])
async def ready() -> dict[str, str | bool]:
    db_ok = check_db_connection()
    return {
        "status": "ready" if db_ok else "not_ready",
        "database": db_ok,
        "service": settings.APP_NAME,
    }


@app.get("/api/v1/", tags=["Root"])
async def api_root() -> dict[str, str]:
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "disabled",
    }