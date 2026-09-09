"""
Main API Router (/api/v1)
"""
from fastapi import APIRouter
from app.api.v1.steganography import router as stego_router
from app.api.v1.analyzer import router as analyzer_router
from app.api.v1.reports import router as reports_router
from app.api.v1.health import router as health_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health_router)
api_v1_router.include_router(stego_router)
api_v1_router.include_router(analyzer_router)
api_v1_router.include_router(reports_router)
