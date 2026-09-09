"""
Health & System Status API Endpoint (/api/v1/health)
"""
from fastapi import APIRouter
from datetime import datetime, timezone
from app.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Returns application status, version, and security configurations."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "security": {
            "max_upload_size_mb": settings.MAX_UPLOAD_SIZE_BYTES // (1024 * 1024),
            "pbkdf2_iterations": settings.PBKDF2_ITERATIONS,
            "cipher": "AES-256-GCM",
            "kdf": "PBKDF2-HMAC-SHA256",
        }
    }
