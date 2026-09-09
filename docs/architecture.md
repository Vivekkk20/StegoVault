# StegoVault System Architecture

StegoVault is an educational cybersecurity and digital-forensics steganography platform. It provides lossless spatial steganography, authenticated encryption, deep statistical steganalysis, dynamic risk scoring, and structured forensic reporting.

---

## 1. High-Level Architectural Decomposition

StegoVault follows a decoupled, multi-tier micro-monolith architecture composed of:
1. **Presentation Layer (Frontend):** A reactive Single Page Application (SPA) developed in React 19, TypeScript, and Tailwind CSS. Provides real-time capacity feedback, interactive steganalysis dashboards (Chart.js), hex visualizers, and a global forensic **Educational Mode**.
2. **Application Layer (Backend API):** A high-performance asynchronous REST API built with FastAPI, Pydantic v2, and Python 3.14. Enforces strict input validation, rate limiting, and zero-trust payload sanitization.
3. **Core Steganography Engine:** Spatial domain Least Significant Bit (LSB) embedding and extraction routines with support for RGB and RGBA color spaces.
4. **Cryptographic Subsystem:** AES-256-GCM authenticated encryption paired with PBKDF2-HMAC-SHA256 (600,000 rounds) key derivation.
5. **Digital Forensics & Steganalysis Engine:** Statistical anomaly detectors calculating Shannon entropy, Chi-Square ($\chi^2$) sample-pair distributions, LSB bit-plane variances, Pearson inter-channel correlation, and raw binary EOF boundaries.
6. **Risk Engine & Reporting Service:** A deterministic 0–100 risk scoring algorithm synthesizing statistical heuristics into actionable forensic verdicts and exportable HTML/JSON reports.

```
+-------------------------------------------------------------------------+
|                           Client Browser (SPA)                          |
|  - React 19 + TypeScript + Tailwind CSS                                 |
|  - Chart.js (RGB Histograms) + HTML5 Canvas (LSB Bit Plane Visualizer)  |
|  - Global Educational Mode Toggle (Deep Forensics Insights)             |
+-------------------------------------------------------------------------+
                                    |
                            HTTP/REST (JSON / FormData)
                                    v
+-------------------------------------------------------------------------+
|                          FastAPI Backend Core                           |
|  - Magic Byte Validation (\x89PNG, BM) & 20MB Size Ceiling             |
|  - Security Middleware (Sanitized Logging, Zero Sensitive Data Leakage)  |
+-------------------------------------------------------------------------+
       |                           |                          |
       v                           v                          v
+------------------+     +--------------------+     +---------------------+
| Steganography    |     | Cryptography       |     | Forensics & Analysis|
| - Spatial LSB    |     | - AES-256-GCM      |     | - Shannon Entropy   |
| - Capacity Meter |     | - PBKDF2 (600k)    |     | - Chi-Square PoV    |
| - 64-byte Header |     | - CSPRNG Nonce/Salt|     | - Pearson Corr.     |
| - CRC32 & SHA-256|     | - Constant-time Cmp|     | - EOF Parser        |
+------------------+     +--------------------+     +---------------------+
                                                              |
                                                              v
                                                    +---------------------+
                                                    | Risk Engine         |
                                                    | - 0-100 Score       |
                                                    | - 13-Section Report |
                                                    | - HTML/JSON Export  |
                                                    +---------------------+
```

---

## 2. Directory Structure

```
stegnography/
|-- backend/
|   |-- app/
|   |   |-- api/v1/endpoints/       # FastAPI route handlers
|   |   |-- core/                   # Config, domain exceptions, secure logging, storage
|   |   |-- security/               # AES-GCM crypto, PBKDF2, SHA streaming, validation
|   |   |-- steganography/          # Binary container, spatial encoder, decoder, capacity
|   |   |-- steganalysis/           # Entropy, LSB, Chi-Square, Histograms, Risk Engine
|   |   `-- main.py                 # FastAPI application factory & middleware
|   |-- tests/                      # Pytest unit, integration, and security test suite
|   |-- reports/                    # Persisted forensic JSON & HTML reports
|   `-- pytest.ini
|-- frontend/
|   |-- src/
|   |   |-- components/             # Reusable UI cards, meters, visualizers, charts
|   |   |-- context/                # Educational Mode React Context
|   |   |-- pages/                  # Dashboard, Encode, Decode, Analyzer, Reports, Settings
|   |   |-- services/               # Typed Axios API client
|   |   |-- types/                  # Strict TypeScript domain interfaces
|   |   `-- App.tsx                 # Root layout & routing
|   |-- package.json
|   `-- vite.config.ts
|-- scripts/
|   |-- generate_test_data.py       # Safe synthetic forensic image generator
|   |-- run_dev.bat                 # One-click Windows dev environment launcher
|   `-- run_tests.bat               # Windows full-stack verification runner
|-- test_data/                      # Synthetic PNG test images (normal, stego, corrupted, etc.)
`-- docs/                           # Comprehensive technical and educational manuals
```

---

## 3. Data Flow & Security Boundaries

### 3.1 Encoding Workflow
1. **Upload & Validation:** Client posts cover image (`image/png` or `image/bmp`), secret text, and passphrase. The backend strictly inspects binary magic bytes (`\x89PNG\r\n\x1a\n` or `\x42\x4d`) and rejects payloads exceeding 20 MB or non-lossless formats.
2. **Key Derivation & Encryption:**
   - 16 bytes of cryptographically secure random salt is generated via `os.urandom(16)`.
   - PBKDF2-HMAC-SHA256 derives a 256-bit encryption key over 600,000 iterations.
   - 12 bytes of fresh CSPRNG nonce is generated.
   - AES-256-GCM produces the ciphertext and a 16-byte cryptographic authentication tag.
3. **Binary Packaging:**
   - The 64-byte binary container header is packed:
     `[4B Magic][2B Version][2B Flags][4B Iterations][16B Salt][12B Nonce][4B Length][16B Tag][4B CRC32]`.
   - Trailer: 32-byte SHA-256 checksum of the entire packed payload.
4. **Spatial Embedding:**
   - Pixel channels ($R, G, B$) are unpacked into flat 1D arrays.
   - The Least Significant Bit ($b_0$) of each successive color byte is modulated:
     $$\text{Pixel}' = (\text{Pixel} \ \& \ \sim 1) \ | \ \text{bit}$$
   - Alpha channel ($A$) is preserved untouched to prevent visual opacity artifacts.
5. **Lossless Export:** The modified pixel buffer is saved to an isolated temporary file as a fresh PNG/BMP image. The cover image is never overwritten. A secure, short-lived download token is returned to the user.

### 3.2 Decoding Workflow
1. **Probe & Header Recovery:**
   - The client uploads an investigation image and passphrase.
   - The engine reads the first $64 \times 8 = 512$ LSB bits to recover the container header.
   - CRC32 checksum over the header is computed and verified in constant time.
   - Magic bytes `STGV` (0x53544756) are checked. If absent, probe detection returns clean.
2. **Payload Extraction & Verification:**
   - The exact ciphertext length $N$ is read from the header.
   - $N$ ciphertext bytes + 32 trailer bytes are extracted from the subsequent pixel LSBs.
   - SHA-256 checksum of the payload container is verified.
3. **Decryption & Authentication:**
   - PBKDF2 derives the AES key using the container's embedded salt and iterations count.
   - AES-256-GCM decrypts and validates the authentication tag. If the tag fails or the key is wrong, an `AuthenticationFailedError` is returned without leaking partial plaintexts.

---

## 4. Forensics & Steganalysis Architecture

The steganalysis subsystem executes concurrently across multiple forensic layers:
1. **File Format & Metadata Parser:**
   - Scans PNG chunk structures (`IHDR`, `IDAT`, `IEND`) or BMP file size headers (`bfSize`).
   - Detects trailing binary data appended past legal EOF boundaries (common in naive steganography).
   - Audits EXIF and non-standard auxiliary chunks.
2. **Shannon Entropy Engine:**
   - Computes Shannon entropy over both raw file bytes and extracted bit planes ($H \in [0, 8]$ for bytes, $H \in [0, 1]$ for bits).
   - Identifies whether the LSB bit plane deviates from natural image entropy toward uniform cryptographic randomness ($H \approx 1.0$).
3. **LSB Chi-Square ($\chi^2$) Analysis:**
   - Measures the statistical equalisation of Pairs of Values (PoV, e.g., $2k$ and $2k+1$) across pixel channels using the Westfeld-Pfitzmann methodology.
4. **Visual Bit-Plane Reconstruction:**
   - Isolates the LSB plane of each color channel, scales bit values ($0 \to 0$, $1 \to 255$), and produces a visual forensic base64 image map highlighting unnatural high-density noise blocks.
5. **Pearson Inter-Channel Correlation:**
   - Measures pairwise correlation coefficients ($r_{RG}, r_{RB}, r_{GB}$). Heavy steganographic injection decorrelates naturally coupled color channels.
6. **Risk Engine:**
   - Computes a calibrated 0–100 risk score and categorizes findings into Clean, Suspicious, or Critical forensic alerts.
