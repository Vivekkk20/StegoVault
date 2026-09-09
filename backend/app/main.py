"""
StegoVault FastAPI Application
Entry point configuring middleware, CORS, security exception handlers, and routing.
"""
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.router import api_v1_router
from app.core.exceptions import StegoVaultException
from app.core.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{settings.APP_NAME} backend initialized successfully.")
    yield
    logger.info(f"{settings.APP_NAME} shutting down.")


app = FastAPI(
    title=settings.APP_NAME,
    description="Educational Cybersecurity & Digital Forensics Steganography Platform",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_logging_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = round((time.time() - start_time) * 1000, 2)
        # Log request without sensitive parameters
        logger.info(
            f"{request.method} {request.url.path} -> {response.status_code} ({process_time}ms)"
        )
        return response
    except Exception as exc:
        process_time = round((time.time() - start_time) * 1000, 2)
        logger.error(
            f"Unhandled exception during {request.method} {request.url.path} after {process_time}ms: {str(exc)}"
        )
        raise exc


@app.exception_handler(StegoVaultException)
async def stegovault_exception_handler(request: Request, exc: StegoVaultException):
    """Handles domain-specific exceptions safely."""
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details,
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Prevents leaking stack traces or internal paths to clients."""
    logger.error(f"Internal server error: {str(exc)}", exc_info=settings.DEBUG)
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred during processing. Security logs have captured this incident.",
        },
    )


# Mount API Router
app.include_router(api_v1_router)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "description": "StegoVault Cybersecurity & Forensic Analysis Engine",
        "api_docs": "/docs" if settings.DEBUG else "Disabled in production",
        "health": "/api/v1/health",
    }
