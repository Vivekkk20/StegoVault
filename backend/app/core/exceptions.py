"""
StegoVault Domain Exceptions
"""

class StegoVaultException(Exception):
    """Base exception for StegoVault domain errors."""
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class FileSecurityError(StegoVaultException):
    """Raised when file validation, magic bytes, or path safety fails."""
    pass


class FileTooLargeError(FileSecurityError):
    """Raised when uploaded file exceeds allowed size limit."""
    pass


class UnsupportedFormatError(StegoVaultException):
    """Raised when an unsupported image format or color mode is provided."""
    pass


class InsufficientCapacityError(StegoVaultException):
    """Raised when the payload exceeds the cover image's embedding capacity."""
    pass


class PayloadError(StegoVaultException):
    """Base exception for payload serialization, decoding, or verification issues."""
    pass


class InvalidPayloadError(PayloadError):
    """Raised when no StegoVault payload header or signature is detected."""
    pass


class CorruptedPayloadError(PayloadError):
    """Raised when payload header CRC or payload SHA-256 checksum check fails."""
    pass


class AuthenticationFailedError(PayloadError):
    """Raised when password key derivation / AES-GCM tag authentication fails."""
    pass


class AnalysisError(StegoVaultException):
    """Raised when an error occurs during forensic steganalysis."""
    pass
