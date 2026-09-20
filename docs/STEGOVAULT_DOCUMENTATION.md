# STEGOVAULT
## Cryptographic Steganography and Steganalysis Toolkit
**StegoVault • Cryptographic Steganography and Steganalysis Toolkit • Vivek Rathod**

---

### Project Overview
- **Project Name:** StegoVault
- **Technical Domain:** Applied Cryptography, Image Steganography, Digital Forensics
- **Core Technologies:** Python 3.14, Streamlit, Pillow (PIL), Cryptography, NumPy, SciPy, pytest
- **Developer:** Vivek Rathod
- **GitHub Repository:** [https://github.com/Vivekkk20/StegoVault](https://github.com/Vivekkk20/StegoVault)
- **Verification Status:** 77 / 77 Automated Tests Passed (100% Automated Test Pass Rate)

> **About StegoVault:**  
> StegoVault is a practical cybersecurity application that combines image steganography, authenticated encryption, image-quality analysis, and defensive steganalysis into an easy-to-use defensive security toolkit.

---

## 1. Introduction & Problem Context

### Short Introduction
In modern digital communications, sending encrypted files through public networks can attract unwanted attention. While encryption scrambles the data so no one else can read it, the scrambled ciphertext itself looks suspicious to network monitors and firewalls. Steganography solves this by hiding the secret data inside ordinary-looking files, such as images.

> 🎯 **Goal:**  
> Provide a practical defense-in-depth security tool that encrypts secret data before hiding it inside innocent-looking images, making sure the data stays both hidden and cryptographically protected.

### What is Steganography?
Steganography is the practice of hiding secret information inside an ordinary, non-suspicious carrier file (such as a digital image). The goal is to conceal the very existence of the communication, so an outsider inspecting the file does not realize that secret data is present.

### What is Encryption?
Encryption is the mathematical process of converting readable plaintext into unreadable ciphertext using a secret key. Without the correct secret key, no unauthorized observer can decrypt or read the underlying information.

### What is the Difference Between Encryption and Steganography?
- **Encryption** protects the *content* of a secret message. An eavesdropper can see that a message is being sent, but cannot read what it says.
- **Steganography** protects the *existence* of the secret message. An eavesdropper sees only an ordinary picture and does not know that a message exists at all.

### Why Hiding Data Inside an Image is Useful
1. **Defensive Privacy:** Allows journalists, whistleblowers, and security researchers operating in heavily monitored environments to transmit sensitive notes without alerting automated keyword scanners.
2. **Covert Storage:** Enables users to store backup credentials, keys, or recovery phrases inside ordinary personal photos.
3. **Defense-in-Depth:** Combining both methods means an attacker must first realize an image contains data, and then still crack military-grade encryption to read it.

### Problems with Basic LSB-Only Approaches
Traditional, basic Least Significant Bit (LSB) steganography tools suffer from two critical security flaws:
1. **No Encryption (Cleartext Hiding):** Naive tools hide raw text directly into pixels. Anyone who extracts the lowest bits instantly recovers the cleartext message.
2. **No Tamper Detection:** If an image is modified in transit or corrupted, raw LSB tools have no way of knowing. They output corrupted text with zero warning.

### Why Encryption Before Embedding Improves Protection
StegoVault follows a strict rule: **Encrypt before embedding**. By encrypting data with **AES-256-GCM** before placing it into the image:
- Even if an adversary extracts every embedded bit, they only obtain random-looking ciphertext.
- Built-in authentication tags detect if even a single bit of the carrier has been tampered with or modified.

### How StegoVault Solves the Problem
StegoVault unites authenticated encryption, lossless image embedding, real-time carrier capacity monitoring, visual quality checks, and forensic detection into one practical tool.

```
+---------------+      +-------------------+      +-------------------------+      +-------------------+
|  Secret Data  | ---> | Encrypt (AES-256) | ---> | Hide in Image (RGB LSB) | ---> | Final Stego Image |
+---------------+      +-------------------+      +-------------------------+      +-------------------+
```

---

## 2. Project Objectives

> 🎯 **Goal:**  
> Build a dependable, verifiable cybersecurity application with clear, practical targets implemented directly in source code.

| Objective | Practical Purpose | Actual Implementation |
|---|---|---|
| **Pre-Embedding Protection** | Scramble secret data using authenticated encryption before it touches the image. | `AES-256-GCM` with a 128-bit GHASH authentication tag (`crypto/encryption.py`) |
| **Brute-Force Resistance** | Prevent dictionary attacks against passphrases using memory-hard key derivation. | `Scrypt` ($N=16384, r=8, p=1$) with a 16-byte random salt (`crypto/key_derivation.py`) |
| **Reliable Data Hiding** | Conceal encrypted bytes sequentially into the spatial color channels of lossless images. | Sequential RGB Least Significant Bit (LSB) embedding (`stego/lsb.py`) |
| **Tamper Detection** | Detect whether an image has been altered or if an incorrect passphrase was entered. | AEAD tag verification during extraction (`core/decoder.py`) |
| **Quality Verification** | Quantify the visual difference between the original image and the stego image. | Real-time Mean Squared Error (MSE) and PSNR calculation (`analysis/image_quality.py`) |
| **Defensive Forensics** | Allow security analysts to audit images for hidden data using visual and statistical tools. | Bit-0 plane slicing and Pairs of Values Chi-Square test (`analysis/steganalysis.py`) |
| **Simple Graphical Interface** | Provide an accessible, clear interface for non-programmers and security analysts. | Interactive local web dashboard built in Streamlit (`app/main.py`) |

---

## 3. Project Scope

> 🎯 **Goal:**  
> Establish clear boundaries between what StegoVault is designed to do and what is deliberately outside its scope.

### In Scope (Fully Implemented & Verified)
- **Lossless Carrier Images:** Full support for PNG, BMP, and TIFF raster images.
- **Payload Types:** Concealment of plain text messages or arbitrary binary files (such as keys, archives, or documents).
- **Authenticated Encryption:** AES-256-GCM with Scrypt key derivation and a 56-byte binary wire envelope (`SVLT`).
- **Dynamic Capacity Meter:** Real-time calculation of carrier capacity with a safe 15% embedding ceiling.
- **Image Quality Measurement:** Fast mathematical calculation of Mean Squared Error (MSE) and Peak Signal-to-Noise Ratio (PSNR).
- **Forensic Steganalysis:** Visual Bit-0 plane extraction and statistical Chi-Square ($\chi^2$) distribution testing.
- **Automated Verification:** 77 comprehensive automated unit and integration tests.

### Out of Scope (Explicit Design Boundaries)
- **Lossy Image Formats (JPEG, WebP):** Lossy compression alters pixel values to save disk space, which permanently destroys LSB data.
- **Network Transmission:** StegoVault is a local application; it does not handle network sockets, cloud uploads, or direct messaging.
- **Public-Key (Asymmetric) Cryptography:** StegoVault uses symmetric passphrase-based cryptography and does not implement PKI certificates or RSA/ECC key pairs.

---

## 4. Tools & Technologies

> 🎯 **Goal:**  
> Use reliable, standard Python libraries to implement every required security, imaging, and UI feature without inventing custom cryptographic primitives.

| Technology | Role in StegoVault | Why It Is Used |
|---|---|---|
| **Python 3.14** | Core programming language | Clean syntax, robust standard libraries, and excellent cryptographic ecosystem. |
| **Streamlit** | Graphical web interface | Enables rapid creation of interactive, professional cybersecurity dashboards. |
| **Pillow (PIL)** | Image processing engine | Reliably opens, inspects, validates, and saves lossless PNG, BMP, and TIFF images. |
| **Cryptography** | Security & encryption | Industry-standard implementation of AES-256-GCM AEAD and Scrypt key derivation. |
| **NumPy** | Vectorized math calculations | Delivers ultra-fast pixel-array calculations for MSE, PSNR, and bit extraction. |
| **SciPy** | Statistical analysis | Computes exact Chi-Square cumulative distribution functions and survival $p$-values. |
| **pytest** | Automated test framework | Executes all 77 automated unit and integration tests to guarantee software quality. |

---

## 5. System Architecture & Data Flow

> 🎯 **Goal:**  
> Provide a transparent, step-by-step explanation of how data travels into the image during encoding and out of the image during decoding.

### Encoding Architecture (Hiding Data)

```
[ Secret Data (Text or File) ]
              ↓
     Step 1: zlib Pre-Compression
              ↓
     Step 2: Scrypt Key Derivation (Passphrase + 16B Random Salt → 256-bit Key)
              ↓
     Step 3: AES-256-GCM Encryption (Plaintext + 12B Nonce → Ciphertext + 16B GHASH Tag)
              ↓
     Step 4: SVLT Binary Wire Framing (Packages 56-byte header with metadata and tag)
              ↓
     Step 5: Sequential RGB LSB Embedding (Bits inserted into Red, Green, Blue lowest bits)
              ↓
   [ Output Stego Image (.png) ]
```

1. **zlib Pre-Compression:** Compresses the secret payload to reduce its size and balance its byte distribution.
2. **Scrypt Key Derivation:** Uses the user's passphrase and a fresh 16-byte random salt to generate a 256-bit encryption key.
3. **AES-256-GCM Encryption:** Encrypts the compressed data using a fresh 12-byte nonce, producing the ciphertext and a 16-byte authentication tag.
4. **SVLT Binary Wire Framing:** Builds an immutable 56-byte header containing magic bytes (`SVLT`), version, salt, nonce, tag, and payload length.
5. **Sequential LSB Embedding:** Reads the header and ciphertext bitstream and embeds each bit sequentially into the lowest bit of the image's RGB channels.
6. **Output Stego Image:** Saves the resulting lossless image ready for transmission or secure storage.

---

### Decoding Architecture (Recovering Data)

```
   [ Stego Image (.png) ]
              ↓
     Step 1: Sequential LSB Bitstream Extraction
              ↓
     Step 2: 56-Byte SVLT Header Parsing & Validation (Magic Bytes & Version)
              ↓
     Step 3: Scrypt Key Re-Derivation (Passphrase + Extracted Salt → 256-bit Key)
              ↓
     Step 4: AEAD Authentication Tag Verification (Checks 16-byte GHASH tag)
              ↓
     Step 5: AES-256-GCM Decryption (Converts ciphertext back to compressed payload)
              ↓
     Step 6: zlib Decompression
              ↓
   [ Original Secret Data Restored ]
```

1. **Sequential LSB Extraction:** Reads the lowest bit of each RGB pixel in order from top-left to bottom-right.
2. **SVLT Header Parsing:** Validates the first 56 bytes to verify the `SVLT` magic identifier and protocol version.
3. **Key Re-Derivation:** Uses the passphrase entered by the receiver and the salt extracted from the header to derive the AES key.
4. **AEAD Authentication:** Recomputes the GHASH tag over the ciphertext and header. If anything was modified, extraction stops immediately.
5. **Decryption & Decompression:** Decrypts the ciphertext and decompresses the bytes to restore the exact original payload.

---

## 6. Application Setup & Installation Guide

> 🎯 **Goal:**  
> Enable any user to set up, launch, and verify StegoVault on a local workstation in under two minutes.

### Step 1: Open the Project Directory
Open your terminal (PowerShell or Command Prompt) and navigate to the project directory:
```powershell
cd d:\projects\stegovault
```

### Step 2: Activate the Python Virtual Environment
Activate the pre-configured virtual environment containing all required libraries:
```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Start the StegoVault Application
Launch the interactive Streamlit dashboard using the application entry point:
```powershell
streamlit run app/main.py
```

### Step 4: Open the Dashboard in Your Web Browser
Streamlit starts a local web server and automatically displays the local URL:
```
Local URL: http://localhost:8501
```
Open your browser and navigate to `http://localhost:8501`.

### Result / Observation
The StegoVault application launches instantly in your browser. The central interface loads with all four functional modules accessible from the top navigation bar.

---

## 7. Practical Walkthrough — Main Dashboard Interface

The main dashboard is the operational hub of StegoVault. It gives users immediate access to all tools while displaying live cryptographic parameters.

> 🎯 **Goal:**  
> Understand the layout of the dashboard, learn how to switch between operational modes, and inspect the active cryptographic configuration.

### What is this?
The main user interface of StegoVault, running locally inside your web browser.

### Why is it used?
It lets security analysts, students, and practitioners perform cryptographic steganography and forensics visually without writing Python scripts.

### How does it work?
Streamlit connects interactive web controls (file uploaders, text areas, buttons, and charts) directly to StegoVault's underlying Python engines in real time.

### Implementation Guide
1. Launch the application and observe the top navigation bar.
2. Notice the four primary operational tabs: **Secure Encode**, **Authenticated Decode**, **Image Quality & Fidelity**, and **Forensic Steganalysis**.
3. Inspect the sidebar on the left side of the screen to verify active cryptographic settings.

![Figure 1: StegoVault Main Interface & Telemetry](screenshots/fig01_dashboard_overview.png)
*Figure 1: StegoVault Main Interface & Telemetry showing navigation tabs, cryptographic engine specifications, and defensive posture indicators.*

### Numbered Highlights & UI Controls
- ① **Mode Switch Navigation Tabs:** Allows one-click switching between the four primary tools (Encode, Decode, Quality, and Steganalysis).
- ② **Sidebar Cryptographic Engine:** Shows verified specifications of active security primitives: `AES-256-GCM` cipher, `Scrypt` memory-hard KDF, `128-bit` GHASH authentication tag, and `16B Salt / 12B Nonce`.
- ③ **StegoVault Header & Architecture Pills:** Displays current operational rules: Defense-in-Depth active, zero third-party cloud dependencies, and lossless carrier enforcement.

### Result / Observation
The user can verify that the system is fully operational, see that cryptographic parameters are correctly initialized, and seamlessly navigate between modules.

---

## 8. Practical Walkthrough — Secure Encoding Workflow

The Secure Encode module encrypts secret data and embeds it into a selected lossless carrier image.

> 🎯 **Goal:**  
> Upload a carrier image, enter a secret message, set a strong passphrase, confirm carrier capacity headroom, and embed the encrypted payload.

### What is this?
The primary workflow where secret information is protected with AES-256-GCM encryption and hidden inside an image's pixel bitstream.

### Why is it used?
To produce an ordinary-looking image that secretly contains confidential information, safe against both interception and tampering.

### How does it work?
When the user clicks the action button, the application compresses the payload, derives an encryption key from the passphrase using Scrypt, encrypts the data with AES-256-GCM, packages the 56-byte SVLT envelope, and modifies the lowest bit of sequential RGB pixels.

### Step-by-Step Implementation Guide
1. **Select Secure Encode:** Click on the **Secure Encode** tab (①).
2. **Upload Carrier Image:** In the **Carrier Ingestion Uploader** (②), click *Browse files* and select a lossless image (`carrier_sample.png`). The preview displays the image with its dimensions.
3. **Enter Secret Payload:** In the **Secret Payload** input area (③), type your secret message or select the *Binary File* option to upload a document.
4. **Enter Passphrase:** In the **Passphrase** field (④), enter your chosen secret passphrase.
5. **Inspect Dynamic Capacity Meter:** Look at the **Capacity Bar** (⑤). Confirm that your payload uses only a small fraction of the available bits (well below the recommended 15% safe ceiling).
6. **Execute Embedding:** Click the **Encrypt & Embed Payload** button (⑥).

![Figure 2: Carrier Upload & Dynamic Capacity Meter](screenshots/fig02_encode_configured.png)
*Figure 2: Carrier Upload & Dynamic Capacity Meter showing image preview, secret payload input, passphrase configuration, and capacity headroom.*

### Numbered Highlights & UI Controls
- ① **Mode Navigation Tab:** "Secure Encode" selected.
- ② **Carrier Ingestion & Preview:** Displays the uploaded carrier image (600x400 PNG) and confirms image dimensions.
- ③ **Secret Payload Input:** Multi-line text field containing the secret message.
- ④ **Cryptographic Passphrase Field:** Secure password field with visibility toggle.
- ⑤ **Dynamic Carrier Capacity Meter:** Real-time progress bar showing payload byte count, total available carrier capacity, and safety zone indicator.
- ⑥ **Action Button:** "Encrypt & Embed Payload" button that triggers the pipeline.

### Result / Observation
The input parameters are validated immediately. The capacity gauge proves that the payload occupies less than 1% of total capacity, ensuring that visual distortion will remain negligible.

---

## 9. Practical Walkthrough — Encoding Execution & Result

Once the embedding process finishes, StegoVault displays execution telemetry, quality metrics, and the download control.

> 🎯 **Goal:**  
> Verify that encryption and embedding succeeded, review mathematical quality metrics, and download the finished stego image.

### What is this?
The post-encoding confirmation screen showing operational telemetry and the generated image.

### Why is it used?
Provides immediate feedback that the data was encrypted without errors, proves mathematically that the image was not visually degraded, and gives the user their output file.

### How does it work?
StegoVault calculates the payload compression ratio, measures the empirical difference between original and stego pixels, and serves the stego image as a lossless PNG download.

### Step-by-Step Implementation Guide
1. Check the green success notification banner at the top of the result area (①).
2. Inspect the **Operational Telemetry Grid** (②) to review original size, encrypted size, MSE, and PSNR.
3. Inspect the **Stego Image Visual Preview** (③) to verify that the image looks identical to the original carrier.
4. Click the **Download Stego Image** button (④) to save `stego_image.png` to your computer.

![Figure 3: Cryptographic Encoding Execution](screenshots/fig03_encode_success.png)
*Figure 3: Cryptographic Encoding Execution showing confirmation banner, mathematical quality metrics, visual preview, and download control.*

### Numbered Highlights & UI Controls
- ① **Success Banner:** "Payload securely encrypted & embedded!" confirmation alert.
- ② **Operational Telemetry Grid:** Metric cards showing payload size (117 B), encrypted envelope size (173 B), Mean Squared Error (**0.000911**), and PSNR (**78.54 dB**).
- ③ **Stego Image Preview:** Visual display of the stego carrier confirming zero visible distortion or color banding.
- ④ **Download Control:** Button allowing one-click download of the resulting `stego_image.png`.

### Result / Observation
The payload was successfully encrypted and embedded. The resulting Peak Signal-to-Noise Ratio of **78.54 dB** confirms that the image modification is mathematically tiny and invisible to the human eye.

---

## 10. Practical Walkthrough — Authenticated Decoding Workflow

The Authenticated Decode module extracts, verifies, and decrypts the secret payload from a stego image.

> 🎯 **Goal:**  
> Upload a stego carrier image, supply the correct passphrase, verify cryptographic integrity, and recover the original secret message.

### What is this?
The extraction workflow where hidden bits are pulled from an image, verified against tampering, and decrypted.

### Why is it used?
Enables authorized recipients who know the secret passphrase to recover the confidential message or file.

### How does it work?
StegoVault extracts sequential LSBs from the image, reads the 56-byte SVLT header, derives the AES-256 key using Scrypt and the embedded salt, validates the 128-bit GHASH authentication tag, and decrypts the payload.

### Step-by-Step Implementation Guide
1. **Select Authenticated Decode:** Click on the **Authenticated Decode** tab (①).
2. **Upload Stego Carrier:** In the file uploader (②), select the stego image (`stego_image.png`).
3. **Enter Passphrase:** Enter the matching secret passphrase into the passphrase field (③).
4. **Click Extract & Decrypt:** Click the **Extract & Decrypt Payload** button.
5. **View Recovered Message:** Read the recovered plaintext message displayed in the output box (④).

![Figure 4: Authenticated Payload Extraction](screenshots/fig04_decode_success.png)
*Figure 4: Authenticated Payload Extraction showing successful authentication, integrity check, and recovered secret plaintext.*

### Numbered Highlights & UI Controls
- ① **Mode Navigation Tab:** "Authenticated Decode" selected.
- ② **Stego Carrier Uploader:** File ingestion area holding the stego image.
- ③ **Passphrase Input Field:** Input field holding the decryption passphrase.
- ④ **Authentication Success & Recovered Payload:** Green alert confirming "Authenticated Payload Extracted Successfully" alongside the recovered cleartext message.

### Result / Observation
The 128-bit GHASH authentication tag verified successfully, proving that neither the image nor the hidden payload was altered in transit. The original secret text was recovered with 100% accuracy.

---

## 11. Security Verification — Tamper Detection & Authentication Failure

A major security benefit of StegoVault is that it detects tampering and wrong passphrases immediately.

> 🎯 **Goal:**  
> Demonstrate how StegoVault prevents unauthorized extraction when given an incorrect passphrase or when pixels have been modified.

### What is this?
The integrity-enforcement capability provided by AES-256-GCM authenticated encryption.

### Why is it used?
Traditional steganography tools output random garbage when given the wrong password, and cannot detect if an attacker modified the hidden data. StegoVault alerts the user immediately and refuses to release unverified data.

### How does it work?
AES-256-GCM recalculates the 128-bit GHASH tag over the ciphertext and header during decryption. If the passphrase is wrong, or if a single bit of the ciphertext or header was changed, the calculated tag will not match the stored tag. StegoVault catches this mismatch and aborts decryption.

### Test Scenarios
- **Scenario A: Incorrect Passphrase Test:** An unauthorized person enters an invalid passphrase (`WrongPassphrase123`).
- **Scenario B: Tampered Image Carrier Test:** An adversary alters pixel values in the carrier image before extraction.

### Step-by-Step Implementation Guide
1. Open the **Authenticated Decode** tab.
2. Upload the valid stego image.
3. In the passphrase field, enter an incorrect passphrase (`WrongPassphrase123`) (①).
4. Click **Extract & Decrypt Payload**.
5. Observe the high-priority red alert banner displayed on screen (②).

![Figure 5: Authentication Failure Telemetry](screenshots/fig05_decode_auth_failure.png)
*Figure 5: Authentication Failure Telemetry showing immediate rejection of extraction when an invalid passphrase or tampered carrier is supplied.*

### Numbered Highlights & UI Controls
- ① **Incorrect Passphrase Input:** User entered an invalid passphrase.
- ② **Red Security Alert Banner:** "Authentication failed! The passphrase is incorrect or the stego image has been tampered with."
- ③ **Defense Explanation:** Telemetry explaining that the AEAD authentication tag failed verification, preventing unauthorized access.

### Result / Observation
StegoVault blocked extraction immediately. Because authentication strictly precedes payload release, an attacker cannot extract partial data or perform chosen-ciphertext bit-flipping attacks.

---

## 12. Practical Walkthrough — Image Quality & Fidelity Analysis

The Image Quality & Fidelity module provides objective mathematical metrics to prove that an image has not been visibly distorted.

> 🎯 **Goal:**  
> Compare the original cover image with the stego image to calculate Mean Squared Error (MSE) and Peak Signal-to-Noise Ratio (PSNR).

### What is this?
An image analysis tool that measures the exact mathematical differences between two images.

### Why is it used?
To verify that hiding data in the image did not create visual artifacts, blurring, or noise that could alert an observer.

### What is MSE (Mean Squared Error)?
MSE measures the average squared difference between corresponding pixel values in the original and stego images:
$$\text{MSE} = \frac{1}{3MN} \sum_{c=1}^3 \sum_{y=1}^M \sum_{x=1}^N \left( I_{\text{cover}}(x,y,c) - I_{\text{stego}}(x,y,c) \right)^2$$
- **Lower is better.** An MSE of zero means the images are identical.

### What is PSNR (Peak Signal-to-Noise Ratio)?
PSNR compares the maximum possible pixel value (255) to the noise introduced by embedding, expressed in decibels (dB):
$$\text{PSNR} = 10 \cdot \log_{10}\left( \frac{255^2}{\text{MSE}} \right)$$
- **Higher is better.** Values above 40 dB are considered visually imperceptible to human eyes. Values above 70 dB indicate near-flawless fidelity.

### Step-by-Step Implementation Guide
1. Click on the **Image Quality & Fidelity** tab (①).
2. Upload both the original cover image and the generated stego image into the comparison viewer (②).
3. Read the calculated Mean Squared Error (MSE) value in the metrics card (③).
4. Read the calculated Peak Signal-to-Noise Ratio (PSNR) value in the metrics card (③).
5. Inspect the visual comparison to confirm that both images look indistinguishable.

![Figure 6: Mathematical Fidelity Analysis](screenshots/fig06_image_quality_fidelity.png)
*Figure 6: Mathematical Fidelity Analysis showing side-by-side comparison, measured MSE (0.000911), and measured PSNR (78.54 dB).*

### Numbered Highlights & UI Controls
- ① **Mode Navigation Tab:** "Image Quality & Fidelity" selected.
- ② **Side-by-Side Image Viewers:** Displays the original cover image alongside the stego image for visual inspection.
- ③ **Quantitative Metrics Card:** Displays measured MSE (**0.000911**) and PSNR (**78.54 dB**) with an automated "Exceptional Fidelity" verdict.

### Result / Observation
For the tested 600x400 image, embedding the encrypted payload resulted in an MSE of **0.000911** and a PSNR of **78.54 dB**. This confirms that the modification affects only 1 out of roughly every 1,100 pixel values by a single unit, making detection by the human eye impossible.

---

## 13. Practical Walkthrough — Forensic Steganalysis (Bit-0 Plane Slicing)

The Forensic Steganalysis module includes defensive diagnostic tools to inspect the lowest bit planes of images.

> 🎯 **Goal:**  
> Extract and visualize the Least Significant Bit plane (Bit 0) of a color channel to inspect the visual footprint created by LSB embedding.

### What is this?
A forensic technique that isolates Bit 0 (the least significant bit) of every pixel across an image channel and displays it as a black-and-white picture.

### Why is it used?
In natural images, pixel values are correlated with their neighbors, creating subtle visual outlines even in the lower bit-planes. When encrypted data is embedded, it introduces completely random bits, replacing natural textures with flat, high-entropy visual noise.

### How does it work?
StegoVault uses NumPy to isolate Bit 0 of each pixel byte in the selected channel (`pixel & 1`) and scales it to display values 0 (black) and 255 (white).

### Step-by-Step Implementation Guide
1. Click on the **Forensic Steganalysis** tab (①).
2. Select the image you want to audit.
3. In the channel selector, choose **Red**, **Green**, or **Blue** (②).
4. Select the **Bit-0 Plane Slice** view.
5. Inspect the resulting visual slice (③). Look for regions where natural image textures transition into random static noise.

![Figure 7: Bit-Plane Forensic Slicing](screenshots/fig07_steganalysis_lsb_plane.png)
*Figure 7: Bit-Plane Forensic Slicing isolating the Bit-0 plane of the carrier to reveal the visual boundary between embedded noise and natural texture.*

### Numbered Highlights & UI Controls
- ① **Mode Navigation Tab:** "Forensic Steganalysis" selected.
- ② **Color Channel & Inspection Selector:** Dropdown controls allowing the user to select the Red, Green, or Blue channel.
- ③ **Bit-0 Plane Visualization:** High-contrast display showing the isolated lowest bits across the image surface.

### Result / Observation
The Bit-0 slice plane clearly shows where sequential LSB embedding occurred: the beginning of the image exhibits high-entropy noise, while the remainder retains the carrier's natural textures. This highlights how defensive forensic analysts detect naive LSB modifications.

---

## 14. Practical Walkthrough — Statistical Steganalysis (Chi-Square Analysis)

StegoVault includes automated statistical testing based on Westfeld and Pfitzmann's Pairs of Values (PoV) method.

> 🎯 **Goal:**  
> Run a mathematical Chi-Square ($\chi^2$) test on adjacent pixel value pairs to calculate the probability that an image contains hidden sequential LSB data.

### What is this?
A statistical detection method that analyzes frequency distributions of adjacent pixel values ($2k$ and $2k+1$) to detect steganography.

### Why is it used?
Visual inspection alone cannot always confirm if an image contains hidden data. Statistical testing provides an automated, mathematical probability score.

### How does it work?
In natural images, pixel values $2k$ and $2k+1$ (such as 100 and 101) occur with different frequencies. When random encrypted bits are embedded into Bit 0, these frequencies become artificially equalized. The Chi-Square test measures this equalization across the image:
$$\chi^2 = \sum_{k=0}^{127} \frac{(n_{2k} - n^*_{2k})^2}{n^*_{2k}} \quad \text{where} \quad n^*_{2k} = \frac{n_{2k} + n_{2k+1}}{2}$$
A survival probability ($p$-value) close to **1.0** indicates that the distribution matches an embedded payload.

### Step-by-Step Implementation Guide
1. In the **Forensic Steganalysis** tab, select **Chi-Square Analysis** (①).
2. Select the target carrier image.
3. Click **Run Chi-Square Analysis**.
4. Read the calculated $\chi^2$ statistic and degrees of freedom (②).
5. Read the calculated survival $p$-value and forensic verdict (③).

![Figure 8: Chi-Square Distribution Analysis](screenshots/fig08_steganalysis_chi_square.png)
*Figure 8: Chi-Square Distribution Analysis displaying the measured Chi-Square statistic, survival p-value, and automated forensic verdict.*

### Numbered Highlights & UI Controls
- ① **Statistical Option Selector:** "Chi-Square Analysis" selected.
- ② **Quantitative Chi-Square Metric:** Displays the calculated $\chi^2$ value and degrees of freedom.
- ③ **Survival Probability ($p$-value) & Forensic Verdict:** Shows the calculated probability score alongside an explanation of the finding.

### Result / Observation
For the tested sample carrier with an embedded sequential payload, the measured $p$-value approached **1.0**, triggering an automated forensic detection alert. This proves the effectiveness of Chi-Square testing for spotting sequential LSB insertion.

---

## 15. Security Implementation & Cryptographic Specifications

> 🎯 **Goal:**  
> Detail the exact security primitives, key derivation parameters, and binary envelope structure implemented in StegoVault.

### AES-256-GCM Authenticated Encryption
- **What is it?** Advanced Encryption Standard in Galois/Counter Mode with 256-bit symmetric keys.
- **What does it do?** Encrypts data for confidentiality while computing a 128-bit GHASH authentication tag for tamper resistance.
- **Why is it used?** Recognized worldwide by NIST (SP 800-38D) as a premier authenticated cipher that protects against both eavesdropping and bit-flipping attacks.

### Scrypt Password-Based Key Derivation (RFC 7914)
- **What is it?** A memory-hard key derivation function designed to resist hardware-accelerated password cracking.
- **What does it do?** Converts the user's passphrase and a random 16-byte salt into a 256-bit AES key.
- **Parameters:** $N = 16384$ (CPU/memory cost), $r = 8$ (block size), $p = 1$ (parallelization), producing a 32-byte key.
- **Why is it used?** Consumes ~16 MiB of RAM per derivation, making GPU/ASIC brute-force attacks prohibitively expensive.

### Salt and Nonce Management
- **Salt (16 Bytes):** Generated fresh for each encryption using the operating system's cryptographic random generator (`os.urandom`). Prevents precomputed rainbow table attacks.
- **Nonce (12 Bytes):** A unique initialization vector generated fresh for each message. Ensures that encrypting the same message twice produces completely different ciphertexts.

### Additional Authenticated Data (AAD)
- **What is it?** Metadata that is authenticated by the cryptographic tag but remains unencrypted in the header.
- **How StegoVault uses it:** The 56-byte SVLT header is bound cryptographically as AAD. If an attacker modifies the header version, flags, or lengths, authentication immediately fails.

### SVLT Binary Wire Envelope Format (56 Bytes)
StegoVault serializes all necessary metadata into an immutable 56-byte binary header placed immediately before the ciphertext:

| Byte Offset | Field Name | Size | Type | Purpose |
|---|---|---|---|---|
| `0x00 - 0x03` | Magic Bytes | 4 Bytes | ASCII (`SVLT`) | Identifies the file as a valid StegoVault payload |
| `0x04` | Version | 1 Byte | `uint8` (`0x01`) | Identifies the protocol version |
| `0x05` | Flags | 1 Byte | Bitmask | Bit 0: Compression (1=zlib); Bit 1: Type (0=text, 1=binary) |
| `0x06 - 0x07` | Reserved | 2 Bytes | `0x0000` | Reserved for future feature extensions |
| `0x08 - 0x17` | Scrypt Salt | 16 Bytes | Raw Bytes | Random salt used for key derivation |
| `0x18 - 0x23` | AES Nonce | 12 Bytes | Raw Bytes | Unique initialization vector for AES-GCM |
| `0x24 - 0x33` | GHASH Tag | 16 Bytes | Raw Bytes | 128-bit authentication tag |
| `0x34 - 0x37` | Payload Length | 4 Bytes | `uint32` (BE) | Length of the encrypted payload in bytes |
| `0x38 - End` | Ciphertext | Variable | Raw Bytes | AES-256-GCM encrypted compressed data |

---

## 16. Verification & Automated Testing Results

> 🎯 **Goal:**  
> Document the automated test suite and confirm that all software components execute without errors or regressions.

StegoVault includes an automated test suite executed with `pytest`. The test suite verifies every layer of the system:

```powershell
pytest
```

### Automated Test Matrix

| Test Suite | Module Under Test | Cases | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| `test_crypto.py` | AES-256-GCM AEAD | 17 | Proper encryption, tag validation, tampered ciphertext rejection, AAD tampering detection | Verified | ✅ Passed |
| `test_key_derivation.py` | Scrypt KDF | 7 | RFC 7914 vector validation, salt uniqueness, parameter verification | Verified | ✅ Passed |
| `test_lsb.py` | Spatial LSB Engine | 12 | Sequential RGB embedding, extraction, RGBA alpha preservation, capacity overflow checks | Verified | ✅ Passed |
| `test_analysis.py` | Quality & Forensics | 16 | MSE and PSNR calculation, Bit-0 plane slicing, Chi-Square statistical calculations | Verified | ✅ Passed |
| `test_utils.py` | Validation & Hashing | 14 | SHA-256 integrity hashing, image header validation, dimension checking | Verified | ✅ Passed |
| `test_integration.py` | End-to-End Pipeline | 11 | Complete encode-then-decode workflows, large binary files, wrong passphrase handling | Verified | ✅ Passed |

### Summary of Test Results
- **Total Tests Executed:** 77
- **Total Tests Passed:** 77
- **Automated Test Pass Rate:** **100%**
- **Execution Time:** 1.92 seconds
- **Regression Status:** Zero regressions, zero missing dependencies, zero deprecated call warnings.

---

## 17. Limitations, Future Scope & Conclusion

### Current Operational Limitations
1. **Lossless Images Only:** StegoVault works strictly with lossless formats (PNG, BMP, TIFF). Messaging platforms (such as WhatsApp, Discord, or Telegram) transcode images to lossy JPEG or WebP, which permanently strips LSB data.
2. **Sequential Embedding Detectability:** Because bits are placed sequentially starting at pixel (0,0), statistical Chi-Square testing can detect the presence of data if the carrier is analyzed.
3. **Capacity Thresholds:** StegoVault enforces a recommended 15% capacity ceiling. Embedding larger payloads will reduce the PSNR below safe thresholds.

### Future Scope & Planned Enhancements
- **PRNG Pixel Scattering:** Use a pseudo-random seed derived from the passphrase to scatter payload bits across pseudo-random pixel locations, evading sequential Chi-Square detection.
- **Adaptive Matrix Encoding (STC):** Implement Syndrome-Trellis Codes to minimize the total number of modified bits per embedded byte.
- **Command-Line Interface (CLI):** Develop an automated CLI tool to allow security teams to embed and extract data within automated defensive pipelines.

### Final Conclusion
StegoVault demonstrates that combining authenticated cryptography (**AES-256-GCM** + **Scrypt**) with image steganography and defensive forensics produces a transparent, verifiable defense-in-depth platform. By ensuring that encryption strictly precedes embedding, StegoVault guarantees that even if steganography is detected, the underlying data remains cryptographically secure against interception and tampering.

---

### Project Attribution
- **Branding:** StegoVault • Cryptographic Steganography and Steganalysis Toolkit • Vivek Rathod
- **Author & Developer:** Vivek Rathod
- **Project Repository:** [https://github.com/Vivekkk20/StegoVault](https://github.com/Vivekkk20/StegoVault)
- **License:** MIT License
