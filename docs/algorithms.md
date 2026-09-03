# StegoVault Algorithms

## 1. Compression

StegoVault compresses the secret data before encryption using the `zlib` compression algorithm.

### Why compression is used

- Reduces payload size.
- Can improve image capacity utilization.
- Makes the encrypted payload independent of the original plaintext structure.

The compressed data is then passed to the encryption stage.

---

## 2. Password-Based Key Derivation

StegoVault uses **Scrypt** to derive a cryptographic key from the user's password.

Scrypt is a memory-hard password-based key derivation function designed to make large-scale password guessing more expensive.

### Parameters

- Key size: 32 bytes (256 bits)
- Salt size: 16 bytes
- Scrypt N: 16384
- Scrypt r: 8
- Scrypt p: 1

A fresh random salt is generated for each encryption operation.

The salt does not need to be secret and is stored inside the payload envelope.

---

## 3. AES-256-GCM

StegoVault uses **AES-256-GCM** for authenticated encryption.

AES provides encryption while GCM provides authentication.

Therefore, the system provides:

- Confidentiality
- Integrity
- Authentication

### Encryption inputs

- 256-bit derived key
- Random 12-byte nonce
- Compressed plaintext
- Additional Authenticated Data (AAD)

The encryption operation produces:

- Ciphertext
- Authentication tag

The authentication tag allows the decoder to detect modification of the encrypted payload.

---

## 4. Binary Envelope

Before embedding, StegoVault packages the encrypted data into a versioned binary envelope.

### Envelope Structure

| Field | Size |
|---|---:|
| Magic | 4 bytes |
| Version | 1 byte |
| Payload Type | 1 byte |
| Reserved | 2 bytes |
| Ciphertext Length | 4 bytes |
| Salt | 16 bytes |
| Nonce | 12 bytes |
| Authentication Tag | 16 bytes |
| Ciphertext | Variable |

The envelope allows the decoder to identify and correctly interpret the embedded payload.

---

## 5. LSB Steganography

StegoVault uses **Least Significant Bit (LSB)** steganography.

Image pixel values contain individual binary bits.

The algorithm replaces selected least significant bits of RGB channel values with payload bits.

Because the least significant bit represents a very small change in the pixel value, the visual difference between the original and stego image is generally small.

### Channel Handling

- RGB channels are used for embedding.
- RGBA images keep the alpha channel unchanged.
- Embedding follows a deterministic sequential traversal.
- Payloads larger than the available capacity are rejected.

---

## 6. Image Quality Metrics

StegoVault provides image quality analysis using:

### Mean Squared Error (MSE)

MSE measures the average squared difference between corresponding pixels of the original and stego images.

Lower MSE generally indicates a smaller pixel-level difference.

### Peak Signal-to-Noise Ratio (PSNR)

PSNR expresses the quality difference between two images in decibels.

Higher PSNR generally indicates greater similarity between the images.

These metrics help evaluate the visual impact of LSB embedding.

---

## 7. Steganalysis

StegoVault includes basic steganalysis features.

### LSB Plane Analysis

The least significant bit plane of an image can be extracted and inspected.

This can help visualize patterns that may be associated with LSB embedding.

### Chi-Square Analysis

Chi-Square analysis provides a statistical indication of whether pixel-value distributions show patterns that may be consistent with LSB embedding.

It is an analytical indicator, not proof that an image contains hidden data.

---

## 8. Complete Algorithm

### Encoding

1. Validate the input.
2. Compress the secret data.
3. Generate a random salt.
4. Derive a 256-bit key using Scrypt.
5. Generate a random AES-GCM nonce.
6. Encrypt the compressed data using AES-256-GCM.
7. Construct the binary envelope.
8. Check image capacity.
9. Embed the envelope using LSB.
10. Save the stego image.

### Decoding

1. Load the stego image.
2. Extract the embedded bitstream.
3. Parse and validate the binary envelope.
4. Extract the salt, nonce, authentication tag, and ciphertext.
5. Derive the key using the supplied password and stored salt.
6. Authenticate and decrypt using AES-256-GCM.
7. Decompress the decrypted data.
8. Return the original text or binary file.

## Important Limitation

LSB steganography does not guarantee invisibility or resistance to detection.

Statistical steganalysis may identify suspicious patterns, and lossy transformations such as JPEG compression or resizing can destroy embedded data.

StegoVault is therefore intended for educational and defensive cybersecurity research rather than guaranteeing undetectable communication.