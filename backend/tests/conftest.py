"""
Pytest Configuration & Fixtures
"""
import io
import sys
from pathlib import Path
import pytest
from PIL import Image
import numpy as np

# Ensure app is importable
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

import os
os.environ["APP_ENV"] = "testing"

from fastapi.testclient import TestClient
from app.config import settings
settings.PBKDF2_ITERATIONS = 1000
from app.main import app


@pytest.fixture
def client():
    """FastAPI test client fixture."""
    return TestClient(app)


@pytest.fixture
def sample_clean_image():
    """Generates a clean synthetic 200x200 RGB image."""
    arr = np.zeros((200, 200, 3), dtype=np.uint8)
    for i in range(200):
        for j in range(200):
            arr[i, j] = [i % 256, j % 256, (i + j) % 256]
    return Image.fromarray(arr, mode="RGB")


@pytest.fixture
def sample_png_bytes(sample_clean_image):
    """Returns PNG bytes of clean sample image."""
    buf = io.BytesIO()
    sample_clean_image.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def sample_bmp_bytes(sample_clean_image):
    """Returns BMP bytes of clean sample image."""
    buf = io.BytesIO()
    sample_clean_image.save(buf, format="BMP")
    return buf.getvalue()
