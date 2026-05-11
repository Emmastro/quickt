import logging
from pathlib import Path

import sentry_sdk
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.core.exceptions import http_exception_handler

from app.domains.auth.router import router as auth_router
from app.domains.agencies.router import router as agencies_router
from app.domains.routes.router import router as routes_router
from app.domains.buses.router import router as buses_router
from app.domains.schedules.router import router as schedules_router
from app.domains.departures.router import router as departures_router
from app.domains.tickets.router import router as tickets_router
from app.domains.payments.router import router as payments_router
from app.domains.trips.router import router as trips_router
from app.domains.notifications.router import router as notifications_router
from app.domains.uploads.router import router as uploads_router

logger = logging.getLogger("quickt")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

settings = get_settings()

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.app_env,
        traces_sample_rate=0.1,
        send_default_pii=False,
    )
    logger.info("Sentry initialized for environment=%s", settings.app_env)

logger.info("QuickT API starting (env=%s)", settings.app_env)

app = FastAPI(
    title="QuickT API",
    description="Online Bus Ticket Platform for Togo",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_exception_handler)

API_V1 = "/api/v1"
app.include_router(auth_router, prefix=f"{API_V1}/auth", tags=["auth"])
app.include_router(agencies_router, prefix=f"{API_V1}/agencies", tags=["agencies"])
app.include_router(routes_router, prefix=f"{API_V1}/routes", tags=["routes"])
app.include_router(buses_router, prefix=f"{API_V1}/buses", tags=["buses"])
app.include_router(schedules_router, prefix=f"{API_V1}/schedules", tags=["schedules"])
app.include_router(departures_router, prefix=f"{API_V1}/departures", tags=["departures"])
app.include_router(tickets_router, prefix=f"{API_V1}/tickets", tags=["tickets"])
app.include_router(payments_router, prefix=f"{API_V1}/payments", tags=["payments"])
app.include_router(trips_router, prefix=f"{API_V1}/trips", tags=["trips"])
app.include_router(notifications_router, prefix=f"{API_V1}/notifications", tags=["notifications"])
app.include_router(uploads_router, prefix=f"{API_V1}/uploads", tags=["uploads"])

# Serve uploaded files (local storage)
if settings.storage_backend == "local":
    uploads_dir = Path(settings.upload_dir)
    uploads_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

# Serve SPA static files in production
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="spa")


@app.get("/api/health", tags=["health"])
async def health_check() -> dict:
    return {"status": "ok", "env": settings.app_env}
