# StegoVault Architecture

## Overview

StegoVault is a cryptographic steganography and steganalysis toolkit designed for educational and defensive cybersecurity use.

The system combines authenticated encryption with image-based Least Significant Bit (LSB) steganography.

## System Pipeline

### Encoding

Secret Data
↓
Compression
↓
Scrypt Key Derivation
↓
AES-256-GCM Encryption
↓
Binary Envelope
↓
LSB Embedding
↓
Stego Image

### Decoding

Stego Image
↓
LSB Extraction
↓
Binary Envelope Parsing
↓
AES-GCM Authentication
↓
Decryption
↓
Decompression
↓
Original Data

## Main Components

### 1. Core

The `core` package manages the main encoding and decoding workflow.

- `encoder.py` — coordinates compression, encryption, envelope creation, and embedding.
- `decoder.py` — extracts, verifies, decrypts, and decompresses hidden data.
- `payload.py` — defines the versioned binary envelope format.
- `exceptions.py` — provides project-specific security and validation errors.

### 2. Cryptography

The `crypto` package provides cryptographic operations.

- `key_derivation.py` — derives a 256-bit encryption key using Scrypt.
- `encryption.py` — provides AES-256-GCM authenticated encryption and decryption.

### 3. Steganography

The `stego` package handles image data embedding.

- `lsb.py` — embeds and extracts payload bits using the Least Significant Bit technique.

Only RGB channels are modified. For RGBA images, the alpha channel is preserved.

### 4. Analysis

The `analysis` package provides image and steganalysis functionality.

- `capacity.py` — calculates available payload capacity.
- `image_quality.py` — calculates image quality metrics such as MSE and PSNR.
- `steganalysis.py` — provides LSB plane inspection and basic Chi-Square analysis.

### 5. Utilities

The `utils` package contains supporting functions such as hashing and input validation.

### 6. Application

The `app` package contains the Streamlit user interface.

It provides separate interfaces for:

- Encoding
- Decoding
- Image Analysis
- Steganalysis

## Security Design

StegoVault follows a defense-in-depth approach.

Encryption is performed before steganographic embedding. Therefore, detecting the existence of a hidden payload does not directly reveal the original plaintext.

AES-256-GCM provides both:

- Confidentiality
- Integrity/authentication

Scrypt is used to derive the encryption key from the user's password.

Fresh random salts and nonces are generated for encryption operations.

## Design Principles

- Use established cryptographic primitives.
- Never store user passwords.
- Do not silently truncate payloads.
- Reject insufficient-capacity carriers.
- Detect authentication failures and corrupted payloads.
- Keep cryptographic logic separate from the user interface.
- Keep analysis functionality separate from encoding and decoding.

## Limitations

StegoVault is an educational and defensive security toolkit.

LSB steganography is not inherently resistant to statistical detection.

Lossy image transformations such as JPEG compression, resizing, or aggressive image processing can destroy embedded data.

Therefore, StegoVault should use lossless image formats such as PNG for reliable storage and transfer.