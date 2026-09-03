"""
StegoVault - Security-Safe Custom Exceptions
Guards against data disclosure and timing leaks by standardizing error reporting.
"""


class StegoVaultError(Exception):
    """Base domain exception for all StegoVault operations."""


class AuthenticationError(StegoVaultError):
    """
    Raised when cryptographic authentication fails (e.g., incorrect passphrase,
    tampered ciphertext, corrupted nonce, or altered AAD).
    Never exposes internal cryptographic details or secret material.
    """


class CorruptPayloadError(StegoVaultError):
    """
    Raised when an extracted or input payload fails binary structural checks,
    magic byte verification, or framing length validation.
    """


class InvalidPayloadError(StegoVaultError):
    """
    Raised when input payload format, flags, or data types are malformed or unsupported.
    """


class InsufficientCapacityError(StegoVaultError):
    """
    Raised when the target carrier cannot accommodate the serialized payload.
    """