"""
StegoVault Cryptographic Engine
Implements authenticated encryption (AES-256-GCM) with PBKDF2-HMAC-SHA256 key derivation.
Zero custom cryptographic implementations; uses standard hazmat primitives.
"""
import os
import zlib
from typing import Tuple
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

from app.core.exceptions import AuthenticationFailedError
from app.config import settings


SALT_SIZE = 16    # 128-bit salt
NONCE_SIZE = 12   # 96-bit standard AES-GCM IV/nonce
TAG_SIZE = 16     # 128-bit authentication tag
KEY_SIZE = 32     # 256-bit AES key


def derive_key(password: str, salt: bytes, iterations: int = settings.PBKDF2_ITERATIONS) -> bytes:
    """
    Derives a 256-bit key from a password and salt using PBKDF2-HMAC-SHA256.
    """
    if not password:
        raise ValueError("Password cannot be empty")
    if len(salt) < SALT_SIZE:
        raise ValueError(f"Salt must be at least {SALT_SIZE} bytes")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt_payload(
    plaintext: bytes,
    password: str,
    associated_data: bytes = b"",
    compress: bool = True,
    iterations: int = settings.PBKDF2_ITERATIONS,
) -> Tuple[bytes, bytes, bytes, bytes, int, int]:
    """
    Encrypts plaintext using AES-256-GCM.
    
    Returns:
        (salt, nonce, ciphertext, auth_tag, flags, iterations)
    """
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    
    flags = 0x01  # Bit 0: AES-256-GCM
    data_to_encrypt = plaintext
    if compress:
        data_to_encrypt = zlib.compress(plaintext, level=9)
        flags |= 0x02  # Bit 1: zlib compressed

    key = derive_key(password, salt, iterations=iterations)
    aesgcm = AESGCM(key)
    
    # AESGCM.encrypt appends the 16-byte authentication tag to the ciphertext
    encrypted = aesgcm.encrypt(nonce, data_to_encrypt, associated_data)
    ciphertext = encrypted[:-TAG_SIZE]
    auth_tag = encrypted[-TAG_SIZE:]
    
    return salt, nonce, ciphertext, auth_tag, flags, iterations


def decrypt_payload(
    ciphertext: bytes,
    auth_tag: bytes,
    password: str,
    salt: bytes,
    nonce: bytes,
    associated_data: bytes = b"",
    flags: int = 0x01,
    iterations: int = settings.PBKDF2_ITERATIONS,
) -> bytes:
    """
    Decrypts and authenticates ciphertext using AES-256-GCM.
    Raises AuthenticationFailedError if password is incorrect or data is tampered.
    """
    if len(auth_tag) != TAG_SIZE:
        raise AuthenticationFailedError("Invalid authentication tag length")
    if len(nonce) != NONCE_SIZE:
        raise AuthenticationFailedError("Invalid nonce length")
    if len(salt) < SALT_SIZE:
        raise AuthenticationFailedError("Invalid salt length")

    key = derive_key(password, salt, iterations=iterations)
    aesgcm = AESGCM(key)
    
    # Reconstruct full encrypted block (ciphertext + tag) for AESGCM.decrypt
    full_encrypted = ciphertext + auth_tag
    try:
        decrypted = aesgcm.decrypt(nonce, full_encrypted, associated_data)
    except InvalidTag:
        raise AuthenticationFailedError(
            "Authentication failed: incorrect password or corrupted ciphertext."
        )

    # Decompress if compression flag is set
    if flags & 0x02:
        try:
            decrypted = zlib.decompress(decrypted)
        except Exception as e:
            raise AuthenticationFailedError(f"Failed to decompress decrypted payload: {str(e)}")

    return decrypted
