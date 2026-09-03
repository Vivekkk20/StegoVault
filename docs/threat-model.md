# StegoVault Threat Model

## Purpose

This threat model describes what StegoVault is designed to protect, the threats it considers, and its security limitations.

StegoVault is an educational and defensive cybersecurity toolkit. It does not guarantee undetectable or perfectly secure communication.

---

## Assets

The main assets protected by StegoVault are:

- Secret text messages
- Secret binary files
- Encryption keys derived from passwords
- Payload integrity
- Embedded data confidentiality

---

## Threat Actors

### 1. Passive Observer

A passive observer can obtain or inspect the stego image but does not know the password.

### Protection

The hidden payload is encrypted using AES-256-GCM before it is embedded.

Therefore, discovering or extracting the embedded ciphertext does not directly reveal the original plaintext.

---

### 2. Active Attacker

An active attacker may modify the stego image.

Possible modifications include:

- Changing pixel values
- Corrupting embedded bits
- Replacing the image
- Modifying the encrypted payload

### Protection

AES-256-GCM authentication allows the decoder to detect modifications to the authenticated encrypted data.

Tampered or corrupted payloads should fail safely instead of returning unauthenticated plaintext.

---

### 3. Password Guessing Attacker

An attacker may attempt to guess the password used to protect the payload.

### Protection

StegoVault derives the encryption key using Scrypt rather than using the password directly.

A random salt is generated for each encryption operation.

However, the overall security against password guessing still depends heavily on the strength of the user's password.

---

### 4. Steganalysis Attacker

An analyst may attempt to determine whether an image contains hidden information.

Possible techniques include:

- Visual inspection
- LSB plane analysis
- Statistical analysis
- Chi-Square analysis

### Limitation

StegoVault's LSB method is not designed to guarantee resistance against advanced steganalysis.

The analysis tools included in StegoVault are primarily educational and defensive.

---

## Security Controls

StegoVault uses several security controls:

### Authenticated Encryption

AES-256-GCM provides encryption and authentication.

### Random Salt

A fresh 16-byte salt is generated for each encryption operation.

### Random Nonce

A fresh 12-byte nonce is generated for AES-GCM encryption.

### Password-Based Key Derivation

Scrypt is used to derive a 256-bit encryption key from the user's password.

### Capacity Validation

The application checks whether the carrier image has enough capacity before embedding.

Payloads are not silently truncated.

### Safe Authentication Failure

Invalid passwords or modified encrypted data result in authentication failure rather than returning unauthenticated plaintext.

---

## Out of Scope

The following threats are outside the primary protection scope of StegoVault:

- Compromised user devices
- Malware or keyloggers
- Passwords intentionally shared with attackers
- Advanced forensic steganalysis
- Recovery of deleted temporary files using forensic techniques
- Security of third-party messaging platforms
- Protection against screenshots or screen recording
- Protection against loss or theft of the user's password

---

## Carrier Limitations

The steganographic carrier must remain compatible with the LSB embedding method.

Lossy operations can damage the hidden payload.

Examples include:

- JPEG compression
- Image resizing
- Cropping
- Some image optimization services
- Other pixel-altering transformations

Lossless PNG images are therefore recommended for reliable use.

---

## Security Assumptions

StegoVault assumes:

1. The user chooses a strong password.
2. The Python cryptographic library is not compromised.
3. The execution environment is trusted.
4. The carrier image is suitable for lossless LSB embedding.
5. The attacker does not have access to the user's password.

---

## Security Goal

The primary security goal is:

> Protect the confidentiality and integrity of the secret payload while demonstrating how cryptography and steganography can be combined in a defense-in-depth architecture.

Steganography provides concealment of the payload's presence, while authenticated encryption protects the payload itself.

These are complementary security mechanisms and should not be treated as substitutes for each other.

---

## Important Disclaimer

StegoVault is an educational and defensive cybersecurity project.

It should not be considered a guarantee of anonymous, undetectable, or unbreakable communication.

Its purpose is to demonstrate secure software design principles, cryptographic concepts, steganography, image analysis, and basic steganalysis.