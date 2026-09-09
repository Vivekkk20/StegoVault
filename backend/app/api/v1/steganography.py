"""
Steganography API Endpoints (/api/v1/steganography)
Handles capacity evaluation, StegoVault payload detection, encoding, decoding, and downloads.
"""
import io
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse

from app.security.validation import validate_image_safe
from app.security.hashes import calculate_sha256
from app.security.sanitization import sanitize_filename
from app.steganography.capacity import evaluate_capacity_for_payload, calculate_image_capacity
from app.steganography.encoder import embed_payload_into_image
from app.steganography.decoder import extract_payload_from_image, detect_stegovault_payload
from app.schemas.steganography import (
    CapacityResponse,
    EncodeResponse,
    DecodeResponse,
    DetectionResponse,
)
from app.core.exceptions import (
    StegoVaultException,
    InsufficientCapacityError,
    InvalidPayloadError,
    CorruptedPayloadError,
    AuthenticationFailedError,
    FileSecurityError,
)
from app.core.logging import logger
from app.config import settings

router = APIRouter(prefix="/steganography", tags=["Steganography"])

# Temporary in-memory token map for generated stego image downloads: token -> filepath
DOWNLOAD_STORE: dict[str, Path] = {}


@router.post("/capacity", response_model=CapacityResponse)
async def check_capacity(
    file: UploadFile = File(...),
    message: str = Form(default=""),
):
    """
    Calculates available lossless LSB capacity of uploaded cover image.
    If message is provided, verifies if capacity is sufficient.
    """
    try:
        content = await file.read()
        img, _ = validate_image_safe(content)
        
        msg_bytes_len = len(message.encode("utf-8")) if message else 0
        result = evaluate_capacity_for_payload(img, msg_bytes_len)
        return result
    except StegoVaultException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.error(f"Error checking capacity: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to evaluate image capacity.")


@router.post("/detect", response_model=DetectionResponse)
async def detect_payload(
    file: UploadFile = File(...)
):
    """
    Probes image for StegoVault header signature without requiring password.
    """
    try:
        content = await file.read()
        img, _ = validate_image_safe(content)
        result = detect_stegovault_payload(img)
        return result
    except StegoVaultException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.error(f"Error detecting payload: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to inspect image header.")


@router.post("/encode", response_model=EncodeResponse)
async def encode_message(
    file: UploadFile = File(...),
    secret_message: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    output_filename: str = Form(default=""),
    compress: bool = Form(default=True),
):
    """
    Encrypts secret_message with password using AES-256-GCM, embeds it into cover image via LSB,
    and returns metadata along with a secure download URL.
    """
    if not secret_message.strip():
        raise HTTPException(status_code=400, detail="Secret message cannot be empty.")
    if not password:
        raise HTTPException(status_code=400, detail="Password cannot be empty.")
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    try:
        content = await file.read()
        cover_img, original_format = validate_image_safe(content)
        cover_hash = calculate_sha256(content)

        # Non-destructive embedding
        stego_img, meta = embed_payload_into_image(
            cover_image=cover_img,
            message=secret_message,
            password=password,
            compress=compress,
        )

        # Determine safe output filename and format (PNG or BMP)
        ext = "bmp" if original_format == "BMP" else "png"
        safe_out_name = sanitize_filename(output_filename, default_ext=ext)

        # Save to temporary storage for download
        token = uuid.uuid4().hex
        out_path = settings.TEMP_DIR / f"{token}_{safe_out_name}"
        save_format = "BMP" if ext == "bmp" else "PNG"
        stego_img.save(out_path, format=save_format)

        with open(out_path, "rb") as f:
            stego_hash = calculate_sha256(f.read())

        DOWNLOAD_STORE[token] = out_path

        return EncodeResponse(
            success=True,
            message="Payload successfully encrypted and embedded into image.",
            output_filename=safe_out_name,
            dimensions=meta["dimensions"],
            mode=meta["mode"],
            payload_bytes=meta["payload_bytes"],
            capacity_bytes=meta["capacity_bytes"],
            capacity_utilization=meta["capacity_utilization"],
            cover_sha256=cover_hash,
            stego_sha256=stego_hash,
            download_url=f"/api/v1/steganography/download/{token}",
        )
    except InsufficientCapacityError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except StegoVaultException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.error(f"Error during encode: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to encode image payload.")


@router.get("/download/{token}")
async def download_stego_image(token: str, background_tasks: BackgroundTasks):
    """
    Serves the generated stego image for download and schedules cleanup.
    """
    file_path = DOWNLOAD_STORE.get(token)
    if not file_path or not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found or download link expired.")

    # Schedule file deletion after serving
    def cleanup():
        DOWNLOAD_STORE.pop(token, None)
        try:
            if file_path.exists():
                file_path.unlink()
        except OSError:
            pass

    background_tasks.add_task(cleanup)
    filename = file_path.name.split("_", 1)[-1]
    media_type = "image/bmp" if filename.lower().endswith(".bmp") else "image/png"

    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename,
    )


@router.post("/decode", response_model=DecodeResponse)
async def decode_message(
    file: UploadFile = File(...),
    password: str = Form(...),
):
    """
    Extracts and decrypts StegoVault hidden payload from uploaded image.
    Safely rejects wrong passwords and corrupted payloads without leaking plaintext.
    """
    if not password:
        raise HTTPException(status_code=400, detail="Password is required to decrypt payload.")

    try:
        content = await file.read()
        stego_img, _ = validate_image_safe(content)
        stego_hash = calculate_sha256(content)

        secret_text, meta = extract_payload_from_image(stego_img, password)

        return DecodeResponse(
            success=True,
            secret_message=secret_text,
            payload_bytes=meta["payload_bytes"],
            ciphertext_bytes=meta["ciphertext_bytes"],
            version=meta["version"],
            compressed=meta["compressed"],
            integrity_verified=meta["integrity_verified"],
            stego_sha256=stego_hash,
        )
    except AuthenticationFailedError:
        # Generic safe error message to prevent oracle/information leaks
        raise HTTPException(
            status_code=401,
            detail="Authentication failed. Incorrect password, or payload has been tampered with."
        )
    except InvalidPayloadError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except CorruptedPayloadError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except StegoVaultException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.error(f"Error during decode: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to extract and decrypt image payload.")
