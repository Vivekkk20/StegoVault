# Spatial LSB Steganography & Binary Container Specification

## 1. Spatial Least Significant Bit (LSB) Theory

Digital raster images represent color values using finite bit depths, typically 8 bits per channel (0–255). An 8-bit color byte can be expressed as:

$$B = \sum_{i=0}^7 b_i \cdot 2^i = b_7 \cdot 128 + b_6 \cdot 64 + \dots + b_1 \cdot 2 + b_0 \cdot 1$$

Where:
- $b_7$ is the **Most Significant Bit (MSB)**, carrying 50% of the perceptual luminance and chromaticity.
- $b_0$ is the **Least Significant Bit (LSB)**, contributing a delta of at most $\pm 1$ unit of intensity out of 255 (a maximum variance of $\approx 0.39\%$).

Because the human visual system (HVS) cannot distinguish an intensity variation of $\Delta = 1$ in ordinary photographic pixels, modulating $b_0$ enables covert data transmission without visible visual distortion.

### Bit Modulation Algorithm
Given an 8-bit channel byte $P$ and a secret payload bit $s \in \{0, 1\}$:
$$P' = (P \ \& \ \text{0xFE}) \ | \ s$$

Where:
- `& 0xFE` (binary `11111110`) clears the LSB to 0.
- `| s` sets the LSB to the payload bit.

Extraction is an identity mask:
$$s = P' \ \& \ \text{0x01}$$

---

## 2. Channel Modulation Strategy

StegoVault operates exclusively on color channels that do not cause visual or rendering glitches:
- **RGB Images:** Bits are sequentially interleaved across the Red ($R$), Green ($G$), and Blue ($B$) channels in raster scan order (row by row, pixel by pixel):
  $$\text{Bit } 0 \to R_{(0,0)}, \quad \text{Bit } 1 \to G_{(0,0)}, \quad \text{Bit } 2 \to B_{(0,0)}, \quad \text{Bit } 3 \to R_{(0,1)}, \dots$$
- **RGBA Images:** The Alpha ($A$) channel governs pixel transparency. Modulating the alpha channel in transparent or semi-transparent regions creates dramatic visual rendering artifacts in web browsers and image viewers. Therefore, StegoVault leaves the Alpha channel completely untouched:
  $$\text{Pixel } = [R', G', B', A_{\text{original}}]$$

---

## 3. The StegoVault Binary Container

StegoVault does not inject raw ASCII text into pixel channels. Doing so produces obvious character clustering in forensic frequency tables and leaves no method for safe boundary detection. Instead, StegoVault packages all payloads into a tamper-evident binary container:

```
+-------------------------------------------------------------------------------+
|                        StegoVault Binary Container Header                     |
|                                     (64 Bytes)                                |
+-----------------------+---------------------+-------------------+-------------+
| Field Name            | Type                | Size              | Offset      |
+-----------------------+---------------------+-------------------+-------------+
| Magic Bytes           | ASCII 'STGV'        | 4 Bytes (0x53...) | 0           |
| Format Version        | uint16 (Big-Endian) | 2 Bytes (0x0001)  | 4           |
| Feature Flags         | uint16 (Big-Endian) | 2 Bytes           | 6           |
| PBKDF2 Iterations     | uint32 (Big-Endian) | 4 Bytes (600,000) | 8           |
| Key Derivation Salt   | CSPRNG Bytes        | 16 Bytes          | 12          |
| AES-GCM Nonce/IV      | CSPRNG Bytes        | 12 Bytes          | 28          |
| Ciphertext Length (N) | uint32 (Big-Endian) | 4 Bytes           | 40          |
| AES-GCM Auth Tag      | Cryptographic Tag   | 16 Bytes          | 44          |
| Header CRC32 Checksum | uint32 (Big-Endian) | 4 Bytes           | 60          |
+-----------------------+---------------------+-------------------+-------------+
|                                PAYLOAD BODY                                   |
|                                (N Bytes)                                      |
+-------------------------------------------------------------------------------+
| Encrypted Ciphertext  | AES-256-GCM Output  | N Bytes           | 64          |
+-------------------------------------------------------------------------------+
|                              PAYLOAD TRAILER                                  |
|                                (32 Bytes)                                     |
+-------------------------------------------------------------------------------+
| Payload SHA-256 Hash  | Binary Digest       | 32 Bytes          | 64 + N      |
+-------------------------------------------------------------------------------+
```

### Total Container Overhead
$$\text{Overhead} = 64 \text{ (Header)} + 32 \text{ (Trailer)} = 96 \text{ Bytes (768 bits)}$$

---

## 4. Embedding Capacity Calculations

The theoretical maximum capacity depends strictly on the number of usable color channels:
$$\text{Usable Channels} = \begin{cases} 3 & \text{for RGB and RGBA} \\ 1 & \text{for Grayscale (L)} \end{cases}$$

$$\text{Total Available Bits} = \text{Width} \times \text{Height} \times \text{Usable Channels}$$
$$\text{Max Payload Capacity (Bytes)} = \left\lfloor \frac{\text{Total Available Bits}}{8} \right\rfloor - 96$$

### Example Capacities
| Image Dimensions | Total Pixels | Available Bits (RGB) | Total Raw Capacity | Max Usable Secret Payload |
| :--- | :--- | :--- | :--- | :--- |
| $256 \times 256$ | 65,536 | 196,608 bits | 24,576 Bytes | 24,480 Bytes (~23.9 KB) |
| $512 \times 512$ | 262,144 | 786,432 bits | 98,304 Bytes | 98,208 Bytes (~95.9 KB) |
| $1920 \times 1080$ | 2,073,600 | 6,220,800 bits | 777,600 Bytes | 777,504 Bytes (~759.2 KB) |

---

## 5. Why Lossless Formats Only (PNG / BMP vs. JPEG)

A critical rule in digital steganography is format preservation. StegoVault strictly accepts **PNG** and **BMP**, while rejecting **JPEG**.

### The Mechanics of JPEG Failure
1. **Discrete Cosine Transform (DCT) Quantization:**
   JPEG does not store raw pixel values. It transforms $8 \times 8$ pixel blocks into spatial frequency components using the Discrete Cosine Transform:
   $$F(u, v) = \frac{1}{4} C(u) C(v) \sum_{x=0}^7 \sum_{y=0}^7 f(x, y) \cos \left[ \frac{(2x+1)u\pi}{16} \right] \cos \left[ \frac{(2y+1)v\pi}{16} \right]$$
2. **High-Frequency Discarding:**
   JPEG divides DCT coefficients by a quantization matrix and rounds them to integers. Because spatial LSB changes manifest as subtle high-frequency noise, JPEG's lossy compression zeroes out or severely alters these frequencies.
3. **Catastrophic Payload Destruction:**
   When a spatial LSB stego-image is saved or converted to JPEG, over $70\%$ to $99\%$ of the modulated LSB bits are permanently corrupted. The 64-byte binary container header CRC32 and SHA-256 checksums immediately fail, rendering payload extraction mathematically impossible.

### Why PNG and BMP are Ideal
- **PNG (Portable Network Graphics):** Uses lossless Deflate compression (LZ77 + Huffman coding) combined with pre-compression prediction filters (Sub, Up, Average, Paeth). Decompressing a PNG yields the exact bit-for-bit pixel buffer.
- **BMP (Bitmap):** Stores uncompressed raw byte arrays with a standard header. Every byte in the pixel array is preserved verbatim.
