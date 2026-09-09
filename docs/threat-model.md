# StegoVault Threat Model & Security Posture

This document evaluates the security architecture, adversary models, and threat vectors of StegoVault using the industry-standard **STRIDE** methodology.

---

## 1. Adversary Models

We analyze StegoVault against three distinct threat actors:

### 1.1 Passive Observer (Eve)
- **Capabilities:** Intercepts network traffic and inspects transmitted images. Has access to standard image viewers and file inspection utilities, but does not possess the secret passphrase.
- **Goal:** Determine whether an image contains hidden data, and if so, read the covert communication.
- **StegoVault Defense:**
  - **Confidentiality:** Guaranteed by AES-256-GCM. The ciphertext is computationally indistinguishable from true random bits. Eve cannot decipher the message.
  - **Stealth:** At low capacity utilization ($< 1\%$), spatial distortions are imperceptible to human eyes and fall below standard automated detection thresholds.

### 1.2 Active Interceptor (Mallory)
- **Capabilities:** Man-in-the-Middle (MitM) position capable of modifying, recompressing, resizing, or manipulating images in transit.
- **Goal:** Forge false messages, alter the plaintext payload, or disrupt covert communication.
- **StegoVault Defense:**
  - **Integrity & Authenticity:** Guaranteed by the 128-bit AES-GCM authentication tag and the 256-bit SHA-256 container trailer.
  - **Tamper Rejection:** Any bit flipped by Mallory invalidates the authentication tag. StegoVault safely rejects tampered images with `AuthenticationFailedError` without executing arbitrary code or disclosing decrypted remnants.
  - **Denial of Service (Image Conversion):** If Mallory converts the image to JPEG or resizes it, the covert data is destroyed. StegoVault detects this as payload loss rather than accepting corrupted plaintext.

### 1.3 Forensic Examiner (Trent)
- **Capabilities:** Equipped with state-of-the-art steganalysis software, statistical test suites (Chi-Square PoV, Sample Pairs Analysis, RS Steganalysis), and raw binary hex parsers.
- **Goal:** Formally prove the presence of steganography for evidentiary or legal purposes.
- **Analysis:**
  - If the embedding rate is high ($> 20\%$), Trent's statistical tests will detect unnatural PoV pairing equalizations ($\chi^2 \to 0$, $p \to 1.0$) and elevated bit entropy ($H \to 1.0$).
  - If StegoVault container detection is executed, the header magic bytes `STGV` provide immediate proof.
  - **Mitigation for Stealth:** When stealth against forensic examiners is required, users must maintain low embedding rates ($< 1\%$ capacity) or use custom flags.

---

## 2. STRIDE Assessment

| Threat Category | Potential Attack Vector | StegoVault Mitigation |
| :--- | :--- | :--- |
| **Spoofing** | Forging an encrypted payload from an unauthorized party | AES-256-GCM authentication tag verifies knowledge of the shared secret key. Unauthorized messages fail authentication. |
| **Tampering** | Modifying image pixels or container headers in transit | 3-tier integrity verification: 32-bit CRC32 header check, 256-bit SHA-256 payload trailer, and 128-bit AES-GCM GHASH tag. |
| **Repudiation** | Denying an image was processed by StegoVault | Forensic SHA-256/SHA-512 hashing records exact byte fingerprints in audit reports. |
| **Information Disclosure** | Extracting secret plaintext without the passphrase | PBKDF2-HMAC-SHA256 (600,000 rounds) + AES-256-GCM. Log redaction ensures keys and plaintexts never appear in logs or error traces. |
| **Denial of Service** | Uploading massive files (e.g. 500 MB) or decompression bombs | Strict 20 MB size ceiling enforced at streaming boundary; Pillow decompression bomb protection active. |
| **Elevation of Privilege** | Remote code execution via malicious image headers or path traversal | Strict magic byte validation (`\x89PNG\r\n\x1a\n` / `\x42\x4d`); sanitized paths (`os.path.basename`); temporary files handled via isolated context managers. |

---

## 3. Assumptions & Cryptographic Bounds

1. **Passphrase Entropy:** The security of PBKDF2 relies on users choosing strong passphrases. Low-entropy passphrases (e.g. "password123") remain susceptible to offline dictionary attacks if the salt is extracted.
2. **Channel Fidelity:** StegoVault assumes a lossless transmission medium. Storage or transit services that re-encode images to JPEG or apply lossy compression will destroy spatial LSB payloads.
3. **Cover Image Cleanliness:** StegoVault assumes cover images are not already pre-contaminated with conflicting steganography or malicious trailing payloads.
