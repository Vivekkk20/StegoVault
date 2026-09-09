"""
Structured Security-Safe Logger for StegoVault
Strictly prevents logging sensitive data (passwords, secrets, keys, plaintext).
"""
import logging
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict


class SecuritySafeJsonFormatter(logging.Formatter):
    """Formats log records as JSON, stripping sensitive fields."""
    
    FORBIDDEN_KEYS = {
        "password", "secret", "key", "plaintext", "cipher", 
        "ciphertext", "auth_tag", "nonce", "salt"
    }

    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include structured extra fields if present
        if hasattr(record, "extra_data") and isinstance(record.extra_data, dict):
            safe_extra = {}
            for k, v in record.extra_data.items():
                if any(forbidden in k.lower() for forbidden in self.FORBIDDEN_KEYS):
                    safe_extra[k] = "[REDACTED]"
                else:
                    safe_extra[k] = v
            log_entry["data"] = safe_extra

        if record.exc_info and record.levelname == "DEBUG":
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def get_logger(name: str = "stegovault") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(SecuritySafeJsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


logger = get_logger()
