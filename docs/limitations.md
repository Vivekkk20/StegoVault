# Known Limitations & Steganographic Frontiers

While StegoVault implements an authenticated and statistically evaluated steganography engine, all spatial-domain steganographic techniques possess inherent physical and mathematical limitations. Understanding these constraints is essential for cybersecurity engineers and digital forensics examiners.

---

## 1. Vulnerability to Lossy Image Recompression

### The Problem
StegoVault operates exclusively in the **spatial domain** by modulating the least significant bit ($b_0$) of individual color channel bytes. Lossy compression algorithms (e.g. JPEG, WebP, HEIC) apply frequency transforms (DCT or Wavelet) and quantize high-frequency coefficients.

### Impact
If a StegoVault stego-image is uploaded to social media platforms (e.g. X/Twitter, Instagram, WhatsApp) or converted to JPEG by an intermediary, lossy recompression irreversibly alters the spatial LSBs. This corrupts the 64-byte container header and renders payload extraction mathematically impossible.

### Mitigation
Transmissions must strictly utilize lossless transport protocols and file formats (PNG or BMP).

---

## 2. Statistical Footprint at High Capacities

### The Problem
StegoVault currently employs **sequential raster embedding**, inserting bits in sequential order across $R, G, B$ channels from the top-left pixel $(0,0)$ downwards.

When embedding payloads that exceed $15–20\%$ of an image's total capacity:
1. **Chi-Square Pairs of Values (PoV):** The Westfeld-Pfitzmann $\chi^2$ test detects artificial equalisation between adjacent even/odd intensity pairs ($2k$ and $2k+1$), causing $p \to 1.0$.
2. **Visual Bit Planes:** The LSB plane visualization displays a stark visual boundary between the noise-saturated stego region and the structured natural image region.

### Future Enhancement: Key-Derived Pseudorandom Permutation (Scatter Embedding)
A robust future enhancement is to disperse bits randomly across the image using a Cryptographic Permutation (e.g., Fisher-Yates shuffle seeded by a key-derived PRNG). This eliminates localized noise clusters and dramatically increases resistance to localized Chi-Square tests.

---

## 3. Vulnerability to Geometric Transformations

Spatial LSB steganography is fragile under basic image transformations:
- **Cropping:** Truncates pixel arrays, destroying header or payload bits.
- **Resizing / Scaling:** Pixel interpolation (bicubic/bilinear) averages neighboring pixel values, overwriting LSB bits.
- **Rotation:** Re-indexes pixel coordinate arrays, destroying bit order.

### Future Enhancement: Transform-Domain Steganography
Embedding in the frequency domain (e.g. Discrete Wavelet Transform, DWT, or Contourlet Transform) offers superior resistance to geometric transformations and print-and-scan attacks.

---

## 4. Resource & Memory Bounds

- **File Size Ceiling:** StegoVault enforces a 20 MB file size limit to prevent Denial of Service (DoS) attacks and excessive memory usage on the backend server.
- **Client-Side Visual Rendering:** Rendering full-resolution $4000 \times 3000$ LSB bit-plane bitmaps directly inside the browser can introduce UI frame drops. StegoVault provides optimized visual previews to balance detail and responsiveness.
