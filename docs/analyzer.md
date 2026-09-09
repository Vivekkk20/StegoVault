# Digital Forensics Steganalysis & Risk Engine

Steganalysis is the science of detecting covert communications hidden within digital media. StegoVault implements an active multi-layer statistical steganalysis suite capable of evaluating structural anomalies, information theory bounds, sample-pair equalizations, and binary file format violations.

---

## 1. Multi-Layer Shannon Entropy Analysis

Entropy quantifies the average rate at which information or uncertainty is produced by a stochastic source of data.

### Byte-Level Shannon Entropy
For a byte sequence $X$ with discrete symbol probabilities $p(x_i)$ for $x_i \in [0, 255]$:

$$H(X) = -\sum_{i=0}^{255} p(x_i) \log_2 p(x_i)$$

- Theoretical Maximum: $H_{\max} = \log_2(256) = 8.0 \text{ bits/byte}$.
- Natural Uncompressed Photographic Images: Typically exhibit $H \approx 6.0 \text{ to } 7.5 \text{ bits/byte}$ due to natural spatial gradients and lighting variations.
- Encrypted or Compressed Payloads: Exhibit maximal disorder, where $H \approx 7.95 \text{ to } 8.0 \text{ bits/byte}$.

### LSB Bit-Plane Entropy
StegoVault extracts the least significant bit $b_0$ across all pixels into an isolated binary stream $B \in \{0, 1\}$:

$$H_{\text{bit}}(B) = - [p(0)\log_2 p(0) + p(1)\log_2 p(1)]$$

- In natural camera images, the physical sensor noise and scene details cause $p(0) \approx 0.45 \text{ to } 0.55$, but localized regions maintain structural order ($H_{\text{bit}} < 0.98$).
- In high-capacity LSB steganography containing ciphertext, the bit stream is pseudorandom and uniformly distributed:
  $$p(0) \approx 0.5000, \quad p(1) \approx 0.5000 \implies H_{\text{bit}} \approx 1.0000$$

---

## 2. Westfeld-Pfitzmann Chi-Square ($\chi^2$) PoV Steganalysis

The Westfeld-Pfitzmann Chi-Square test is the gold standard statistical attack against sequential spatial LSB replacement.

### Theoretical Basis: Pairs of Values (PoV)
In an 8-bit image, the LSB operation partitions the 256 intensity values into 128 disjoint pairs of adjacent values:
$$\text{PoV}_k = \{2k, \ 2k+1\}, \quad k \in [0, 127]$$

For example:
$$\{0, 1\}, \ \{2, 3\}, \ \{4, 5\}, \ \dots, \ \{254, 255\}$$

When an embedding algorithm replaces the LSB of pixel value $2k$ with a random bit:
- If the bit is 0, the value remains $2k$.
- If the bit is 1, the value becomes $2k+1$.

Similarly, when embedding into $2k+1$:
- If the bit is 0, the value transitions to $2k$.
- If the bit is 1, the value remains $2k+1$.

Because AES-GCM ciphertext bits have an equal probability $p(0) = p(1) = 0.5$, embedding hidden data forces the frequencies of $2k$ and $2k+1$ toward perfect equality:
$$E_k = \frac{h(2k) + h(2k+1)}{2}$$

Where $h(v)$ is the observed frequency count of pixel intensity $v$.

### Test Statistic & p-Value
The test compares observed frequencies against the expected equalized distribution:

$$\chi^2 = \sum_{k=0}^{127} \frac{(h(2k) - E_k)^2}{E_k}$$

With degrees of freedom $df = 127$ (omitting zero-count pairs). The $p$-value represents the probability that the observed sample fits the theoretical equalized hypothesis:

$$p = 1 - \frac{1}{\Gamma(df/2)} \int_0^{\chi^2/2} t^{df/2 - 1} e^{-t} dt$$

- **Natural Image:** Frequencies of $2k$ and $2k+1$ naturally differ ($h(2k) \neq h(2k+1)$), yielding a large $\chi^2$ distance and $p \approx 0.0$.
- **Stego-Image (LSB Embedded):** As embedding density increases, $\chi^2$ drops toward zero and $p \to 1.0$, indicating a high probability of artificial manipulation.

---

## 3. Pearson Inter-Channel Correlation

In natural color photography, the Red, Green, and Blue channels exhibit high mutual correlation due to shared scene illumination, textures, and geometry:
$$r_{X, Y} = \frac{\sum_{i=1}^N (X_i - \bar{X})(Y_i - \bar{Y})}{\sqrt{\sum_{i=1}^N (X_i - \bar{X})^2} \sqrt{\sum_{i=1}^N (Y_i - \bar{Y})^2}}$$

StegoVault calculates:
- $r_{RG} = \text{Corr}(\text{Red}, \text{Green})$
- $r_{RB} = \text{Corr}(\text{Red}, \text{Blue})$
- $r_{GB} = \text{Corr}(\text{Green}, \text{Blue})$

While natural images maintain $r \ge 0.85$, heavy independent pseudorandom modulation in the spatial domain reduces inter-channel correlation.

---

## 4. Visual Bit-Plane Extraction

StegoVault isolates the $b_0$ plane of each channel and renders it to a high-contrast forensic bitmap:
$$V(x, y) = \begin{cases} 255 & \text{if } P(x, y) \ \& \ 1 = 1 \\ 0 & \text{if } P(x, y) \ \& \ 1 = 0 \end{cases}$$

- **Natural Image LSB Plane:** Shows clear contours, silhouettes, and shadows of the photographed subject matter.
- **Embedded LSB Plane:** The embedded region appears as an unnatural, sharply demarcated block of white-noise static, contrasting starkly with the structured contours of the unencoded region.

---

## 5. File Format Parsing & Trailing Data Detection

Attackers frequently append data directly past the legal End-Of-File (EOF) marker to hide messages without modifying pixel data. StegoVault audits the low-level byte structure:

### PNG Analysis
- Walks chunk sequence: `IHDR` $\to$ `IDAT` $\dots \to$ `IEND`.
- The legal termination of a PNG stream occurs exactly 4 bytes past the `IEND` type identifier (accounting for the 4-byte CRC):
  $$\text{Legal EOF} = \text{Offset}(\text{IEND}) + 4 \text{ (Chunk Name)} + 4 \text{ (CRC)}$$
- If $\text{Physical File Size} > \text{Legal EOF}$, any trailing bytes are extracted, hashed, and flagged as an anomaly.

### BMP Analysis
- Inspects the 14-byte Bitmap File Header.
- Reads `bfSize` at offset 2 (4-byte unsigned integer).
- If $\text{Physical File Size} > \text{bfSize}$, the surplus data is identified as an appended covert payload.

---

## 6. Calibrated 0–100 Risk Score Engine

The StegoVault Risk Engine synthesizes the forensic metrics into a deterministic 0–100 severity index:

```
+-------------------------------------------------------------+
| Metric Contribution Breakdown                               |
+------------------------------------+------------------------+
| Indicator                          | Maximum Score Added    |
+------------------------------------+------------------------+
| StegoVault Magic Container Detected| +85 Points             |
| Appended Trailing Data Past EOF    | +45 Points             |
| Chi-Square p-Value (p >= 0.90)     | +30 Points             |
| LSB Bit Distribution Deviation     | +20 Points             |
| LSB Entropy Anomaly (H >= 0.999)   | +15 Points             |
| Non-Standard Metadata / Chunks     | +10 Points             |
+------------------------------------+------------------------+
```

### Risk Classification Thresholds
- **Clean ($0 \le \text{Score} \le 20$):** No anomalous patterns detected. Statistical metrics conform to typical photographic baselines.
- **Suspicious ($21 \le \text{Score} \le 55$):** Mild statistical irregularities observed (e.g., elevated LSB entropy or non-standard metadata). Further manual investigation recommended.
- **Critical ($56 \le \text{Score} \le 100$):** High-confidence detection. Conclusive evidence of hidden steganographic payload, container headers, or appended EOF payloads.
