# StegoVault — Cryptographic Steganography & Steganalysis Toolkit

StegoVault is a professional cybersecurity toolkit designed to integrate authenticated cryptography, spatial-domain image steganography, and statistical steganalysis into an educational and practical defensive platform.

## Key Tenets
- **Defense-in-Depth:** Encryption precedes steganographic embedding. If steganography is detected, ciphertext remains protected under standard security models.
- **Integrity First:** Authenticated encryption (AEAD) ensures silent tampering or carrier corruption triggers verification failures.
- **Zero Inventions:** Strictly leverages vetted, standard primitives from the Python `cryptography` ecosystem.
- **Forensic Visibility:** Features tools for carrier capacity checking, perceptual difference analysis (MSE, PSNR), and statistical detection (LSB plane slicing, Chi-Square analysis).

## Core Pipeline
1. **Encode:** Payload -> Compression -> Authenticated Encryption (AES-256-GCM) -> Binary Envelope -> LSB Carrier Embedding -> Stego Image
2. **Decode:** Stego Image -> Bitstream Extraction -> Envelope Parsing -> AEAD Tag Verification & Decryption -> Decompression -> Original Payload

## Notice on Carrier Channels
Social media and messaging applications (such as WhatsApp, Discord, Twitter, and Telegram) transcode, compress, or convert images to lossy formats (JPEG/WebP). This permanently strips LSB data. Carriers must be transmitted as uncompressed/lossless files (e.g., PNG, BMP).