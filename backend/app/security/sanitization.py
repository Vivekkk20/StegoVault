"""
Filename Sanitization & Temporary Storage Manager
Guarantees path traversal prevention and ensures automatic file cleanup.
"""
import re
import os
import uuid
import tempfile
from pathlib import Path
from contextlib import contextmanager
from typing import Generator
from app.config import settings
from app.core.exceptions import FileSecurityError


def sanitize_filename(filename: str, default_ext: str = "png") -> str:
    """
    Sanitizes user-provided filename:
    - Strips directory components and path traversal sequences.
    - Limits to alphanumeric characters, dashes, underscores, and dots.
    - Guarantees safe extension.
    """
    if not filename:
        return f"stegovault_output_{uuid.uuid4().hex[:8]}.{default_ext}"

    # Extract only the base name (no directory paths)
    base = os.path.basename(filename.replace("\\", "/"))
    
    # Strip any directory traversal remnants
    base = base.replace("..", "").strip(" /\\")

    # Replace forbidden chars with underscore
    sanitized = re.sub(r"[^a-zA-Z0-9_\.-]", "_", base)
    
    # Remove leading dots to prevent hidden files
    sanitized = sanitized.lstrip(".")

    if not sanitized:
        sanitized = f"stegovault_{uuid.uuid4().hex[:8]}"

    # Validate extension
    if not (sanitized.lower().endswith(".png") or sanitized.lower().endswith(".bmp")):
        sanitized = f"{sanitized}.{default_ext}"

    return sanitized


@contextmanager
def safe_temp_file(suffix: str = ".png") -> Generator[Path, None, None]:
    """
    Context manager creating a temporary file inside settings.TEMP_DIR,
    automatically unlinking it upon exit.
    """
    temp_dir = settings.TEMP_DIR
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / f"tmp_{uuid.uuid4().hex}{suffix}"
    
    try:
        yield temp_path
    finally:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass
