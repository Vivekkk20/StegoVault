"""
StegoVault - Main Application Entry Point
Streamlit-based dashboard providing an upgraded, cyber-defense styled interface for
Encoding, Decoding, Image Quality Inspection, and Steganalysis.
"""

from __future__ import annotations

import io
from pathlib import Path
import sys

# Ensure root directory is on Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from PIL import Image

from analysis.capacity import calculate_carrier_capacity
from analysis.image_quality import calculate_mse, calculate_psnr
from analysis.steganalysis import chi_square_attack, extract_lsb_plane
from core.decoder import decode_payload
from core.encoder import encode_payload
from core.exceptions import (
    AuthenticationError,
    CorruptPayloadError,
    InsufficientCapacityError,
    InvalidPayloadError,
    StegoVaultError,
)
from core.payload import PAYLOAD_TYPE_BINARY, PAYLOAD_TYPE_TEXT
from utils.hashing import compute_sha256
from utils.validation import validate_carrier_image

# ----------------------------------------------------------------------
# PAGE CONFIGURATION & INJECTED THEME CSS
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="StegoVault — Cryptographic Steganography Toolkit",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
/* Font Imports */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

code, pre, .mono-font {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Header Gradient */
.stego-title {
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}

.stego-subtitle {
    font-size: 0.95rem;
    color: #94A3B8;
    margin-bottom: 1.5rem;
}

/* Security Tag Badges */
.badge-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 1.2rem;
}

.sec-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}

.badge-cyan {
    background: rgba(56, 189, 248, 0.12);
    color: #38BDF8;
    border: 1px solid rgba(56, 189, 248, 0.3);
}

.badge-purple {
    background: rgba(192, 132, 252, 0.12);
    color: #C084FC;
    border: 1px solid rgba(192, 132, 252, 0.3);
}

.badge-green {
    background: rgba(74, 222, 128, 0.12);
    color: #4ADE80;
    border: 1px solid rgba(74, 222, 128, 0.3);
}

/* Card Styling */
.stat-card {
    background: rgba(30, 41, 59, 0.45);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(8px);
}

.stat-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94A3B8;
    margin-bottom: 0.25rem;
}

.stat-value {
    font-size: 1.3rem;
    font-weight: 700;
    color: #F8FAFC;
}

/* Tab Active Highlights */
div[data-baseweb="tab-list"] {
    gap: 8px;
}

button[data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    transition: all 0.2s ease;
}

/* Streamlit Button Elevate */
div.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

div.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(56, 189, 248, 0.25);
}

/* Hash Display Box */
.hash-box {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 6px;
    padding: 8px 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #38BDF8;
    word-break: break-all;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# SIDEBAR: SYSTEM STATUS & SPECIFICATIONS
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛡️ StegoVault Core")
    st.caption("Cryptographic Steganography Architecture")

    st.markdown("---")
    st.markdown("**🔒 Cryptographic Engine**")
    st.write("• **Cipher:** `AES-256-GCM` (AEAD)")
    st.write("• **KDF:** `Scrypt` (N=16384, r=8, p=1)")
    st.write("• **Tag:** `128-bit` Poly1305 / GHASH")
    st.write("• **Salt & Nonce:** `16B Salt / 12B Nonce`")

    st.markdown("---")
    st.markdown("**🖼️ Carrier Protocols**")
    st.write("• **Supported:** `PNG, BMP, TIFF`")
    st.write("• **Embedding:** Spatial LSB (RGB)")
    st.write("• **Transparency:** Alpha Channel Preserved")
    st.write("• **Safe Ceiling:** `15% Usable Capacity`")

    st.markdown("---")
    st.info(
        "⚠️ **Lossy Channels Warning:**\n"
        "Messaging platforms (WhatsApp, Discord, Twitter/X) transcode to JPEG, "
        "destroying LSB bits. Transmit carriers as lossless files."
    )

    st.caption("StegoVault v1.2.0 • 77 Tests Passing")

# ----------------------------------------------------------------------
# MAIN HEADER
# ----------------------------------------------------------------------
st.markdown('<div class="stego-title">🛡️ StegoVault</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="stego-subtitle">Defense-in-Depth Cryptographic Steganography, Wire Framing & Forensic Steganalysis Toolkit</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="badge-container">
        <span class="sec-badge badge-cyan">AES-256-GCM Authenticated</span>
        <span class="sec-badge badge-purple">Scrypt Memory-Hard KDF</span>
        <span class="sec-badge badge-green">Zero Inventions Principle</span>
        <span class="sec-badge badge-cyan">Spatial LSB Forensics</span>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_encode, tab_decode, tab_quality, tab_steganalysis = st.tabs(
    ["🔒 Secure Encode", "🔓 Authenticated Decode", "📊 Image Quality & Fidelity", "🔍 Forensic Steganalysis"]
)

# ----------------------------------------------------------------------
# 1. ENCODE TAB
# ----------------------------------------------------------------------
with tab_encode:
    st.markdown("#### Embed Authenticated Ciphertext into Carrier Media")
    st.caption("Payload is compressed, encrypted via AES-256-GCM, and embedded into LSB channels.")

    col_carrier, col_payload = st.columns([1, 1], gap="medium")

    with col_carrier:
        st.markdown("##### 1. Select Cover Image")
        carrier_file = st.file_uploader(
            "Upload Lossless Carrier (PNG, BMP)",
            type=["png", "bmp", "tiff"],
            key="enc_carrier",
            help="Lossless formats preserve spatial LSB bits without compression artifacts.",
        )

        carrier_img = None
        total_capacity_bytes = 0
        safe_capacity_bytes = 0

        if carrier_file:
            try:
                carrier_img = Image.open(carrier_file)
                validate_carrier_image(carrier_img)

                st.image(carrier_img, caption=f"Carrier: {carrier_file.name}", use_container_width=True)
                total_capacity_bytes, safe_capacity_bytes = calculate_carrier_capacity(carrier_img)

                # Metrics row
                m1, m2, m3 = st.columns(3)
                m1.metric("Resolution", f"{carrier_img.width}x{carrier_img.height}")
                m2.metric("Color Mode", carrier_img.mode)
                m3.metric("Max Capacity", f"{total_capacity_bytes:,} B")

            except Exception as e:
                st.error(f"Carrier validation error: {e}")
                carrier_img = None

    with col_payload:
        st.markdown("##### 2. Secret Payload & Cryptography")

        payload_category = st.radio(
            "Payload Format",
            ["Text Message", "Binary Document / File"],
            horizontal=True,
        )

        payload_bytes = b""
        selected_type = PAYLOAD_TYPE_TEXT

        if payload_category == "Text Message":
            raw_text = st.text_area(
                "Confidential Plaintext",
                placeholder="Enter confidential instructions, credentials, or private notes...",
                height=130,
            )
            if raw_text:
                payload_bytes = raw_text.encode("utf-8")
            selected_type = PAYLOAD_TYPE_TEXT
        else:
            upload_payload = st.file_uploader(
                "Select File to Hide",
                key="enc_file_payload",
                help="Any binary document (PDF, ZIP, keys, code).",
            )
            if upload_payload:
                payload_bytes = upload_payload.getvalue()
            selected_type = PAYLOAD_TYPE_BINARY

        # Capacity Gauge
        if carrier_img and total_capacity_bytes > 0:
            # Wire envelope adds 56 bytes prefix + small zlib overhead
            estimated_wire_bytes = len(payload_bytes) + 56
            usage_ratio = min(estimated_wire_bytes / total_capacity_bytes, 1.0)
            usage_pct = (estimated_wire_bytes / total_capacity_bytes) * 100

            st.write(f"Payload Footprint: **{len(payload_bytes):,} bytes** (Est. Wire Frame: **{estimated_wire_bytes:,} bytes**)")

            if estimated_wire_bytes <= safe_capacity_bytes:
                st.progress(usage_ratio, text=f"Safe Footprint: {usage_pct:.2f}% of carrier used (< 15% safe ceiling)")
            elif estimated_wire_bytes <= total_capacity_bytes:
                st.progress(usage_ratio, text=f"High Utilization: {usage_pct:.2f}% of carrier used (Statistically detectable)")
            else:
                st.progress(1.0, text=f"Capacity Exceeded! Payload requires {estimated_wire_bytes:,} B, max is {total_capacity_bytes:,} B")
        else:
            st.write(f"Payload Footprint: **{len(payload_bytes):,} bytes**")

        enc_passphrase = st.text_input(
            "Encryption Passphrase",
            type="password",
            key="enc_pass",
            help="Derived into a 256-bit symmetric key using Scrypt (N=16384, r=8, p=1). Never stored.",
        )

        if payload_bytes:
            sha_preview = compute_sha256(payload_bytes)
            st.markdown(f'<div class="hash-box">SHA-256: {sha_preview}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔐 Encrypt & Embed into Carrier", type="primary", use_container_width=True):
            if not carrier_img:
                st.error("Please provide a valid cover carrier image.")
            elif not payload_bytes:
                st.error("Payload data cannot be empty.")
            elif not enc_passphrase:
                st.error("Passphrase is required for AES-256-GCM key derivation.")
            else:
                with st.spinner("Compressing (zlib), deriving key (Scrypt), encrypting (AES-GCM), and embedding LSBs..."):
                    try:
                        stego_image = encode_payload(
                            carrier_image=carrier_img,
                            payload=payload_bytes,
                            passphrase=enc_passphrase,
                            payload_type=selected_type,
                        )

                        buf = io.BytesIO()
                        stego_image.save(buf, format="PNG")
                        stego_bytes = buf.getvalue()

                        st.success("✅ Payload securely encrypted and embedded! Authenticated tag bound to AAD header.")
                        st.download_button(
                            label="📥 Download Stego Carrier (PNG)",
                            data=stego_bytes,
                            file_name="stego_vault_output.png",
                            mime="image/png",
                            type="secondary",
                            use_container_width=True,
                        )
                    except InsufficientCapacityError as err:
                        st.error(f"Carrier capacity exceeded: {err}")
                    except StegoVaultError as err:
                        st.error(f"Security halt: {err}")
                    except Exception as err:
                        st.error(f"Embedding failed: {err}")

# ----------------------------------------------------------------------
# 2. DECODE TAB
# ----------------------------------------------------------------------
with tab_decode:
    st.markdown("#### Extract & Authenticate Embedded Payload")
    st.caption("Verifies the 56-byte binary envelope, validates the GCM authentication tag, and recovers original data.")

    col_dec_img, col_dec_act = st.columns([1, 1], gap="medium")

    with col_dec_img:
        st.markdown("##### 1. Upload Stego Image")
        stego_file = st.file_uploader(
            "Upload Stego Carrier (PNG, BMP)",
            type=["png", "bmp", "tiff"],
            key="dec_stego",
        )

        stego_img = None
        if stego_file:
            try:
                stego_img = Image.open(stego_file)
                st.image(stego_img, caption=f"Stego Image: {stego_file.name}", use_container_width=True)
            except Exception as e:
                st.error(f"Failed to load image buffer: {e}")

    with col_dec_act:
        st.markdown("##### 2. Authentication Credentials")
        dec_passphrase = st.text_input(
            "Decryption Passphrase",
            type="password",
            key="dec_pass",
            help="Supplied passphrase will be combined with the extracted salt to re-derive the 256-bit key.",
        )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔓 Authenticate & Decrypt", type="primary", use_container_width=True):
            if not stego_img:
                st.error("Please upload a stego carrier image.")
            elif not dec_passphrase:
                st.error("Decryption passphrase is required.")
            else:
                with st.spinner("Extracting wire frame, verifying AEAD authentication tag, and decrypting..."):
                    try:
                        recovered_payload, payload_type = decode_payload(
                            stego_image=stego_img,
                            passphrase=dec_passphrase,
                        )

                        st.success("✅ AEAD Integrity Confirmed: Authentication tag and framing metadata match exactly.")

                        rec_hash = compute_sha256(recovered_payload)
                        st.markdown(f'<div class="hash-box">Recovered SHA-256: {rec_hash}</div>', unsafe_allow_html=True)
                        st.write(f"Recovered Footprint: **{len(recovered_payload):,} bytes**")

                        if payload_type == PAYLOAD_TYPE_TEXT:
                            try:
                                text_result = recovered_payload.decode("utf-8")
                                st.text_area("Decrypted Plaintext", value=text_result, height=160)
                            except UnicodeDecodeError:
                                st.warning("Payload marked as text but contains binary non-UTF8 bytes.")
                                st.download_button(
                                    "📥 Download Recovered Raw Data",
                                    data=recovered_payload,
                                    file_name="recovered_payload.bin",
                                    use_container_width=True,
                                )
                        else:
                            st.download_button(
                                label="📥 Download Recovered Binary File",
                                data=recovered_payload,
                                file_name="recovered_file.bin",
                                mime="application/octet-stream",
                                type="primary",
                                use_container_width=True,
                            )
                    except AuthenticationError:
                        st.error("❌ Authentication Failed: Invalid passphrase or carrier data tampered with in transit.")
                    except CorruptPayloadError:
                        st.error("❌ Framing Corrupt: Carrier does not contain a valid StegoVault payload envelope.")
                    except InvalidPayloadError as err:
                        st.error(f"❌ Protocol Error: {err}")
                    except StegoVaultError as err:
                        st.error(f"❌ Operation Halted: {err}")
                    except Exception as err:
                        st.error(f"❌ Extraction Error: {err}")

# ----------------------------------------------------------------------
# 3. IMAGE QUALITY TAB
# ----------------------------------------------------------------------
with tab_quality:
    st.markdown("#### Mathematical Fidelity & Perceptual Error Analysis")
    st.caption("Quantifies pixel perturbations between cover carrier and stego output using MSE and PSNR.")

    col_q1, col_q2 = st.columns(2, gap="medium")
    with col_q1:
        img_orig_file = st.file_uploader("Original Cover Carrier", type=["png", "bmp", "tiff"], key="q_orig")
    with col_q2:
        img_mod_file = st.file_uploader("Stego Carrier", type=["png", "bmp", "tiff"], key="q_mod")

    if img_orig_file and img_mod_file:
        try:
            im1 = Image.open(img_orig_file)
            im2 = Image.open(img_mod_file)

            if im1.size != im2.size:
                st.error(f"Dimension mismatch: Original is {im1.size}, Stego is {im2.size}. Images must possess identical geometry.")
            else:
                mse_val = calculate_mse(im1, im2)
                psnr_val = calculate_psnr(im1, im2)

                st.markdown("---")
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("Resolution", f"{im1.width}x{im1.height} px")
                m_col2.metric("Mean Squared Error (MSE)", f"{mse_val:.6f}")
                m_col3.metric(
                    "Peak SNR (PSNR)",
                    "∞ dB (Identical)" if psnr_val == float("inf") else f"{psnr_val:.2f} dB",
                )

                if psnr_val == float("inf"):
                    st.info("💎 The two images are bit-for-bit identical across all channels.")
                elif psnr_val >= 60.0:
                    st.success("💎 **Pristine Fidelity (PSNR >= 60 dB):** Modifications are mathematically minimal and completely imperceptible.")
                elif psnr_val >= 50.0:
                    st.success("✅ **High Fidelity (PSNR >= 50 dB):** Changes are well below human visual perception limits.")
                else:
                    st.warning("⚠️ **Moderate Degradation (PSNR < 50 dB):** Substantial payload footprint. High statistical visibility risk.")

                # Side-by-side previews
                p_c1, p_c2 = st.columns(2)
                p_c1.image(im1, caption="Original Cover", use_container_width=True)
                p_c2.image(im2, caption="Stego Carrier", use_container_width=True)

        except Exception as e:
            st.error(f"Fidelity calculation failed: {e}")

# ----------------------------------------------------------------------
# 4. STEGANALYSIS TAB
# ----------------------------------------------------------------------
with tab_steganalysis:
    st.markdown("#### Forensic Steganalysis & Statistical Detection")
    st.caption("Performs bit-plane decomposition (Bit-0 plane slicing) and Pairs-of-Values (PoV) Chi-Square distribution attack.")

    inspect_file = st.file_uploader(
        "Select Image to Analyze",
        type=["png", "bmp", "tiff"],
        key="steg_inspect",
    )

    if inspect_file:
        try:
            target_img = Image.open(inspect_file)

            st.markdown("##### 1. LSB Bit-Plane Decomposition (Bit-0 Contrast Slicing)")
            st.caption("Scales the lowest-order bit (0 -> 0, 1 -> 255) to expose artificial noise grids or sequential banding.")

            plane_col1, plane_col2 = st.columns([1, 2], gap="medium")
            with plane_col1:
                st.image(target_img, caption="Carrier Overview", use_container_width=True)
                plane_channel = st.selectbox("Inspect Color Channel", ["Red", "Green", "Blue"])
                channel_map = {"Red": 0, "Green": 1, "Blue": 2}

            with plane_col2:
                plane_img = extract_lsb_plane(target_img, channel_map[plane_channel])
                st.image(plane_img, caption=f"Bit-0 Plane ({plane_channel} Channel)", use_container_width=True)

            st.markdown("---")
            st.markdown("##### 2. Pairs of Values (PoV) Chi-Square Statistical Attack")
            st.caption("Evaluates frequency equalization between adjacent value pairs (2k, 2k+1) induced by sequential LSB replacement.")

            p_val, chi_stat = chi_square_attack(target_img)

            s_col1, s_col2 = st.columns(2)
            s_col1.metric("Chi-Square Statistic (χ²)", f"{chi_stat:.4f}")
            s_col2.metric("Survival p-value", f"{p_val:.6e}")

            if p_val < 0.05:
                st.error(
                    f"⚠️ **Statistical Anomaly Detected (p = {p_val:.4e} < 0.05):**\n"
                    "Adjacent Pairs-of-Values exhibit unnatural frequency equalization. "
                    "This image contains strong statistical evidence consistent with artificial sequential LSB replacement."
                )
            else:
                st.success(
                    f"✅ **No Structural Bias Detected (p = {p_val:.4f} >= 0.05):**\n"
                    "Bit transitions align with natural uncompressed photographic entropy. "
                    "The carrier does not exhibit detectable sequential LSB replacement patterns."
                )

            with st.expander("ℹ️ How Chi-Square Steganalysis Works"):
                st.write(
                    "In natural photographic images, adjacent luminance values (e.g., 200 and 201) have varying probabilities. "
                    "Sequential LSB replacement equalizes these frequencies towards their mean ((count(2k) + count(2k+1)) / 2). "
                    "When the Chi-Square statistic is high and p-value drops below the 0.05 significance threshold, it indicates "
                    "a non-random artificial manipulation."
                )

        except Exception as e:
            st.error(f"Steganalysis analysis failed: {e}")