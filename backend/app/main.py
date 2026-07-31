"""FastAPI application entry point.

Run locally with:
    uvicorn backend.app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.analytics import router as analytics_router
from backend.api.detection import router as detection_router
from backend.api.explainability import router as explainability_router
from backend.api.prevention import router as prevention_router
from backend.app.api.routes.detection_routes import router as prediction_router
from backend.app.config import get_settings
from backend.app.database import close_mongo_connection, connect_to_mongo


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for real-time phishing website detection and prevention.",
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.allowed_origins,
#     allow_origin_regex=settings.allowed_origin_regex,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # "http://localhost:5174",
        # "http://127.0.0.1:5174",
        # "http://localhost:3000",
        # "http://127.0.0.1:3000"
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    """Initialize external resources when the API starts."""

    await connect_to_mongo()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Release external resources when the API stops."""

    await close_mongo_connection()


@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    """Simple health endpoint for uptime checks and load balancers."""

    return {"status": "ok", "service": settings.app_name}


app.include_router(detection_router, prefix=settings.api_prefix)
app.include_router(prevention_router, prefix=settings.api_prefix)
app.include_router(explainability_router, prefix=settings.api_prefix)
app.include_router(analytics_router, prefix=settings.api_prefix)
app.include_router(prediction_router)
app.include_router(explainability_router)
app.include_router(analytics_router)
