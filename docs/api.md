# StegoVault REST API Specification

The StegoVault backend exposes a versioned REST API (`/api/v1`) with JSON payloads and `multipart/form-data` endpoints for file handling.

---

## Base URL
```
http://127.0.0.1:8000/api/v1
```

Interactive OpenAPI Swagger UI is available at:
```
http://127.0.0.1:8000/docs
```

---

## 1. System Endpoints

### `GET /health`
Returns system status, cryptographic defaults, and runtime configuration.

#### Response (`200 OK`)
```json
{
  "status": "healthy",
  "app_name": "StegoVault",
  "version": "1.0.0",
  "environment": "production",
  "crypto": {
    "algorithm": "AES-256-GCM",
    "kdf": "PBKDF2-HMAC-SHA256",
    "pbkdf2_iterations": 600000,
    "magic_bytes": "STGV"
  }
}
```

---

## 2. Steganography Endpoints

### `POST /steganography/capacity`
Calculates lossless LSB embedding capacity and validates whether a proposed message fits.

#### Request (`multipart/form-data`)
- `file` (File, required): Target cover image (PNG or BMP).
- `message` (string, optional): Secret message text to evaluate.

#### Response (`200 OK`)
```json
{
  "dimensions": [1920, 1080],
  "format": "PNG",
  "channels": 3,
  "total_pixels": 2073600,
  "available_bits": 6220800,
  "total_capacity_bytes": 777600,
  "max_usable_payload_bytes": 777504,
  "estimated_payload_bytes": 142,
  "capacity_utilization_percent": 0.02,
  "is_sufficient": true
}
```

---

### `POST /steganography/encode`
Encrypts plaintext using AES-256-GCM and embeds the container into the image's spatial LSBs.

#### Request (`multipart/form-data`)
- `file` (File, required): Cover image (PNG or BMP).
- `message` (string, required): Secret plaintext.
- `password` (string, required): Encryption passphrase (minimum 8 characters).

#### Response (`200 OK`)
```json
{
  "success": true,
  "download_token": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "filename": "stego_cover.png",
  "file_size_bytes": 1048576,
  "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "sha512": "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e",
  "capacity_used_percent": 0.04,
  "crypto_metadata": {
    "algorithm": "AES-256-GCM",
    "kdf": "PBKDF2-HMAC-SHA256",
    "iterations": 600000,
    "salt_hex": "6a9f8b...",
    "nonce_hex": "012345...",
    "auth_tag_hex": "fa81bc...",
    "ciphertext_length": 142
  }
}
```

---

### `GET /steganography/download/{token}`
Downloads the encoded stego-image associated with a valid download token.

#### Response (`200 OK`)
- Binary file stream (`image/png` or `image/bmp`) with `Content-Disposition: attachment; filename="stego_filename.png"`.

---

### `POST /steganography/decode`
Extracts and decrypts a hidden payload from an uploaded image.

#### Request (`multipart/form-data`)
- `file` (File, required): Candidate stego-image.
- `password` (string, required): Decryption passphrase.

#### Response (`200 OK`)
```json
{
  "success": true,
  "plaintext": "Confidential research findings...",
  "payload_length": 34,
  "extracted_at": "2026-09-09T14:30:00Z",
  "crypto_metadata": {
    "algorithm": "AES-256-GCM",
    "kdf": "PBKDF2-HMAC-SHA256",
    "iterations": 600000,
    "salt_hex": "6a9f8b...",
    "nonce_hex": "012345...",
    "auth_tag_hex": "fa81bc...",
    "ciphertext_length": 50
  },
  "file_hashes": {
    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "sha512": "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e"
  }
}
```

#### Error Responses
- `400 Bad Request`: CRC32 verification failed or image does not contain a StegoVault payload.
- `401 Unauthorized`: Password incorrect or authentication tag verification failed.

---

### `POST /steganography/detect`
Performs a fast probe of an image to check for a StegoVault header without needing the passphrase.

#### Request (`multipart/form-data`)
- `file` (File, required): Candidate image.

#### Response (`200 OK`)
```json
{
  "has_stegovault_payload": true,
  "confidence": 1.0,
  "details": {
    "version": 1,
    "flags": 0,
    "iterations": 600000,
    "ciphertext_length": 142
  }
}
```

---

## 3. Steganalysis & Forensics Endpoints

### `POST /analyzer/analyze`
Executes full multi-layer statistical steganalysis and generates a forensic report.

#### Request (`multipart/form-data`)
- `file` (File, required): Image to inspect.

#### Response (`200 OK`)
Returns the complete 13-section analysis report (metadata, cryptographic hashes, Shannon byte & bit entropy, Chi-Square test, visual bit plane, RGB histograms, channel correlations, trailing data detection, risk score, and technical findings).

---

### `GET /reports`
Lists all persisted forensic analysis reports with summary risk scores and timestamps.

---

### `GET /reports/{report_id}`
Retrieves the complete JSON representation of a stored report.

---

### `GET /reports/{report_id}/export`
Downloads a self-contained, standalone forensic HTML report document.

---

## 4. Example `curl` Commands

### Encode a Hidden Message
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/steganography/encode" \
  -F "file=@cover.png" \
  -F "message=Cybersecurity forensics demonstration" \
  -F "password=SuperSecurePassphrase2026!"
```

### Decode Hidden Message
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/steganography/decode" \
  -F "file=@stego_cover.png" \
  -F "password=SuperSecurePassphrase2026!"
```

### Run Forensics Analysis
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/analyzer/analyze" \
  -F "file=@evidence.png"
```
