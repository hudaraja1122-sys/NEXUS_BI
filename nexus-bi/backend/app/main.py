"""NEXUS BI backend entrypoint."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.datasets import router as datasets_router
from app.api.analysis import router as analysis_router

settings = get_settings()

app = FastAPI(
    title="NEXUS BI API",
    description="Autonomous AI Business Intelligence Analyst — backend service.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(datasets_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")


@app.get("/health", tags=["system"])
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "nexus-bi-backend",
        "environment": getattr(settings, "environment", "development"),
    }


@app.get("/", tags=["system"])
def root() -> dict:
    return {"message": "NEXUS BI API — see /docs for interactive schema."}