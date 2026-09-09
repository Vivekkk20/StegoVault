# StegoVault: Secure Steganography & Digital Forensics Platform

<div align="center">

```
  ____  _                      __     __            _ _   
 / ___|| |_ ___  __ _  ___    \ \   / /_ _ _   _| | |_ 
 \___ \| __/ _ \/ _` |/ _ \____\ \ / / _` | | | | | __|
  ___) | ||  __/ (_| | (_) |____\ V / (_| | |_| | | |_ 
 |____/ \__\___|\__, |\___/      \_/ \__,_|\__,_|_|\__|
                |___/                                   
```

**An educational cybersecurity and digital forensics steganography & steganalysis suite.**  
*Lossless Spatial LSB Embedding • AES-256-GCM Cryptography • Deep Statistical Steganalysis • Forensic Risk Engine*

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19.0-61DAFB.svg?logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7%2B-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Tests](https://img.shields.io/badge/Tests-43%20Passed-brightgreen.svg)](#testing)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## Executive Summary

StegoVault is a full-stack, enterprise-grade steganography and digital-forensics analysis platform. Designed from scratch for security researchers, forensic investigators, and students, StegoVault bridges the gap between theoretical information hiding and real-world cryptographic defense.

Unlike rudimentary steganography tools that inject unauthenticated plaintext into pixels, StegoVault combines:
1. **Authenticated Encryption (AES-256-GCM)** with OWASP-recommended **PBKDF2-HMAC-SHA256** key derivation (600,000 iterations).
2. A **tamper-evident 64-byte binary container** featuring Magic bytes (`STGV`), format versioning, PBKDF2 round counts, CSPRNG salt & nonce, CRC32 header integrity, and a 32-byte SHA-256 payload trailer.
3. An active **forensic steganalysis engine** evaluating Shannon byte and bit entropy, LSB 0/1 distributions, Westfeld-Pfitzmann Chi-Square ($\chi^2$) sample-pair tests, 256-bin RGB histograms, Pearson inter-channel correlation, and raw binary EOF boundaries.
4. A calibrated **0–100 transparent risk score** producing itemized technical findings and exportable standalone forensic HTML/JSON reports.
5. A dark, modern **cybersecurity operations dashboard** featuring a global toggleable **Educational Mode** explaining the underlying mathematical and forensic mechanics at every step.

---

## System Architecture

```
+-------------------------------------------------------------------------+
|                        Frontend Dashboard (SPA)                         |
|  - React 19 + TypeScript + Tailwind CSS                                 |
|  - Chart.js RGB Histograms + HTML5 Canvas LSB Bit-Plane Visualizer      |
|  - Global Educational Mode Toggle (Forensics & Cryptography Context)   |
+-------------------------------------------------------------------------+
                                    |
                            HTTP/REST (JSON / Multipart)
                                    v
+-------------------------------------------------------------------------+
|                          FastAPI Backend Core                           |
|  - Magic Byte Validation (\x89PNG, BM) & 20MB Security Size Ceiling    |
|  - Sanitized Logging (Zero Leakage of Keys, Nonces, or Passwords)       |
+-------------------------------------------------------------------------+
       |                           |                          |
       v                           v                          v
+------------------+     +--------------------+     +---------------------+
| Steganography    |     | Cryptography       |     | Forensics & Analysis|
| - Spatial LSB    |     | - AES-256-GCM      |     | - Shannon Entropy   |
| - Capacity Meter |     | - PBKDF2 (600k)    |     | - Chi-Square PoV    |
| - 64-byte Header |     | - CSPRNG Nonce/Salt|     | - Pearson Corr.     |
| - CRC32 & SHA-256|     | - Constant-time Cmp|     | - Trailing Data EOF |
+------------------+     +--------------------+     +---------------------+
                                                              |
                                                              v
                                                    +---------------------+
                                                    | Risk Engine         |
                                                    | - Calibrated 0-100  |
                                                    | - 13-Section Report |
                                                    | - HTML / JSON Export|
                                                    +---------------------+
```

---

## Core Capabilities

### 1. Spatial Domain Lossless Steganography
- **Lossless Formats:** Exclusively targets PNG and BMP images. Lossy formats (JPEG) are strictly rejected with clear educational guidance explaining why DCT quantization destroys spatial LSB bits.
- **Channel Isolation:** Modulates the Red, Green, and Blue ($R, G, B$) channels sequentially. The Alpha ($A$) channel is kept untouched to prevent transparency artifacts.
- **Real-Time Capacity Estimation:** Instantly evaluates cover image resolution and usable bit limits before encoding begins.

### 2. Zero-Trust Cryptographic Engine
- **AES-256-GCM:** Authenticated symmetric encryption with a 128-bit authentication tag guarantees confidentiality and tamper detection.
- **PBKDF2-HMAC-SHA256:** Converts user passphrases into 256-bit keys using a fresh 16-byte CSPRNG salt over 600,000 iterations.
- **Header-Embedded Metadata:** The iteration count and salt are stored inside the container header, allowing seamless cross-environment portability without hardcoded settings.
- **Constant-Time Verification:** All integrity checks utilize `hmac.compare_digest` to defeat side-channel timing attacks.

### 3. Deep Forensics & Steganalysis Engine
- **Multi-Layer Shannon Entropy:** Evaluates both whole-file byte entropy ($H \in [0, 8]$) and LSB bit-plane entropy ($H_{\text{bit}} \in [0, 1]$).
- **Westfeld-Pfitzmann Chi-Square ($\chi^2$) Test:** Measures the statistical equalization of adjacent Pairs of Values (PoV, $2k$ and $2k+1$) across color channels.
- **Visual Bit-Plane Reconstruction:** Renders high-contrast base64 bitmaps isolating the least significant bit plane to visually expose artificial noise boundaries.
- **Pearson Inter-Channel Correlation:** Computes pairwise correlation coefficients ($r_{RG}, r_{RB}, r_{GB}$) to detect decorrelation induced by heavy steganographic embedding.
- **Binary File Format Parsing & EOF Detection:** Traverses PNG chunk structures (`IHDR` $\to$ `IDAT` $\dots \to$ `IEND`) or BMP file size headers (`bfSize`) to identify covert payloads appended past legal termination markers.

### 4. Deterministic Risk Engine & 13-Section Reports
- Calibrates statistical indicators into a transparent 0–100 severity index (**Clean**, **Suspicious**, or **Critical**).
- Assembles comprehensive 13-section digital forensics reports.
- One-click exports to standalone, print-ready HTML dossiers and machine-readable JSON files.

---

## Project Structure

```
stegnography/
|-- backend/
|   |-- app/
|   |   |-- api/v1/endpoints/       # FastAPI route controllers
|   |   |-- core/                   # Configuration, exceptions, secure logging, report storage
|   |   |-- security/               # AES-GCM, PBKDF2, streaming SHA, magic byte validation
|   |   |-- steganography/          # Binary container, spatial encoder, decoder, capacity meter
|   |   |-- steganalysis/           # Entropy, LSB, Chi-Square, histograms, risk engine
|   |   `-- main.py                 # Application factory, CORS, exception handlers
|   |-- tests/                      # 43 automated Pytest test cases
|   |-- reports/                    # Persisted forensic reports
|   `-- pytest.ini
|-- frontend/
|   |-- src/
|   |   |-- components/             # Reusable UI cards, meters, visualizers, charts
|   |   |-- context/                # Educational Mode React context provider
|   |   |-- pages/                  # Dashboard, Encode, Decode, Analyzer, Reports, Settings, About
|   |   |-- services/               # Axios REST API client
|   |   |-- types/                  # Strict TypeScript domain interfaces
|   |   `-- App.tsx                 # Root layout & page routing
|   |-- package.json
|   `-- vite.config.ts
|-- scripts/
|   |-- generate_test_data.py       # Safe synthetic test image generator
|   |-- run_dev.bat                 # One-click Windows dev launcher (Backend + Frontend)
|   `-- run_tests.bat               # Automated test & build verification suite
|-- test_data/                      # Safe synthetic test images
`-- docs/                           # In-depth architectural & theoretical documentation
```

---

## Quick Start & Installation

### Prerequisites
- **Python 3.10+** (tested on Python 3.14)
- **Node.js 18+** & **npm** (tested on Node v24)
- Windows / macOS / Linux

### Automated Windows Launcher
For Windows users, launch both services with one click:
```cmd
scripts\run_dev.bat
```
Or run the complete verification test suite:
```cmd
scripts\run_tests.bat
```

---

### Manual Setup

#### 1. Backend Service
```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- **Backend API:** `http://127.0.0.1:8000`
- **Interactive Swagger Docs:** `http://127.0.0.1:8000/docs`

#### 2. Frontend Dashboard
```bash
cd frontend
npm install
npm run dev
```
- **Frontend Dashboard:** `http://127.0.0.1:5173`

---

## Testing & Quality Assurance

StegoVault includes a comprehensive automated test suite of **43 test cases** spanning cryptography, binary containers, LSB steganography, statistical forensics, file format boundary security, and API endpoints.

To run the Pytest suite:
```bash
cd backend
.venv\Scripts\pytest -v
```

### Test Coverage Highlights
- `test_crypto.py`: AES-256-GCM roundtrips, wrong password rejection, tampered ciphertext rejection, tampered auth tag rejection.
- `test_payload.py`: 64-byte container packing/unpacking, CRC32 header verification, corrupted CRC rejection.
- `test_steganography.py`: Lossless capacity evaluation, RGB/RGBA encoding/decoding, overflow prevention.
- `test_steganalysis.py`: Shannon byte & bit entropy bounds, Chi-Square PoV test, 256-bin RGB histograms, Pearson correlation matrix, trailing data detection past legal EOF.
- `test_security.py`: Magic byte enforcement against fake extensions, rejection of lossy formats (JPEG), 20MB file size ceiling enforcement, decompression bomb protection, path traversal sanitization.
- `test_dataset.py`: Automatic validation of all synthetic test images.
- `test_api.py`: Full HTTP roundtrips across all endpoints.

---

## Synthetic Test Dataset

Generate the synthetic test images with:
```bash
python scripts/generate_test_data.py
```
Generated artifacts in `test_data/`:
1. `normal.png` — Natural photographic gradient baseline (**Clean**, Risk $\le 20$).
2. `stego_low.png` — StegoVault container with short payload ($< 1\%$ capacity).
3. `stego_medium.png` — StegoVault container with moderate payload.
4. `stego_high.png` — Dense payload occupying $> 50\%$ capacity (**Triggers Chi-Square & Bit Entropy anomalies**).
5. `corrupted.png` — Valid container with flipped LSB bits (**Tests tamper detection**).
6. `metadata_test.png` — PNG with custom comment and timestamp chunks.
7. `trailing_data_test.png` — PNG with 191 bytes appended past legal `IEND` chunk.

---

## In-Depth Documentation

For complete technical specifications, review the dedicated manuals in `docs/`:
- **[System Architecture](docs/architecture.md)** — Modular design, data flows, and security boundaries.
- **[Steganography Engine](docs/steganography.md)** — Spatial LSB theory, bit slicing, 64-byte container format, and capacity mathematics.
- **[Cryptographic Architecture](docs/encryption.md)** — AES-256-GCM, PBKDF2-HMAC-SHA256, salt/nonce randomness, and tamper detection.
- **[Steganalysis & Risk Engine](docs/analyzer.md)** — Shannon entropy, Westfeld-Pfitzmann Chi-Square test, histograms, and risk scoring.
- **[Threat Model](docs/threat-model.md)** — STRIDE evaluation, adversary models (Eve, Mallory, Trent), and security bounds.
- **[REST API Specification](docs/api.md)** — Complete endpoint schemas, request/response formats, and `curl` examples.
- **[Testing Strategy](docs/testing.md)** — Automated test design and dataset verification.
- **[Known Limitations](docs/limitations.md)** — Constraints of spatial LSB steganography and future research frontiers.

---

## Educational Disclaimer

StegoVault is developed strictly for educational, defensive, and digital-forensics research purposes. It is designed to illustrate how steganographic communications operate, how cryptographic protection prevents unauthorized decipherment, and how statistical forensics techniques detect covert channels.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
