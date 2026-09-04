"""
StegoVault - Main Application Entry Point
Streamlit-based dashboard providing user interfaces for Encoding,
Decoding, Image Quality Inspection, and Steganalysis.
"""

from __future__ import annotations

import io
import streamlit as st
from PIL import Image

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
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

st.set_page_config(
    page_title="StegoVault Toolkit",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ StegoVault")
st.caption("Cryptographic Steganography & Steganalysis Toolkit")

tab_encode, tab_decode, tab_quality, tab_steganalysis = st.tabs(
    ["🔒 Encode", "🔓 Decode", "📊 Image Quality", "🔍 Steganalysis"]
)

# ----------------------------------------------------------------------
# 1. ENCODE TAB
# ----------------------------------------------------------------------
with tab_encode:
    st.header("Embed Encrypted Payload")
    carrier_file = st.file_uploader(
        "Upload Carrier Image (PNG, BMP)",
        type=["png", "bmp"],
        key="enc_carrier",
    )

    if carrier_file:
        try:
            carrier_img = Image.open(carrier_file)
            st.image(carrier_img, caption="Carrier Preview", width=300)

            total_bytes, safe_bytes = calculate_carrier_capacity(carrier_img)
            st.info(
                f"Carrier Dimensions: {carrier_img.width}x{carrier_img.height} | "
                f"Mode: {carrier_img.mode} | "
                f"Max Usable: {total_bytes} bytes | "
                f"Recommended Safe Ceiling (15%): {safe_bytes} bytes"
            )

            payload_category = st.radio(
                "Payload Type",
                ["Text Message", "Binary File"],
                horizontal=True,
            )

            payload_bytes = b""
            selected_type = PAYLOAD_TYPE_TEXT

            if payload_category == "Text Message":
                raw_text = st.text_area("Secret Message", placeholder="Type confidential data...")
                payload_bytes = raw_text.encode("utf-8") if raw_text else b""
                selected_type = PAYLOAD_TYPE_TEXT
            else:
                upload_payload = st.file_uploader("Select Secret File", key="enc_file_payload")
                if upload_payload:
                    payload_bytes = upload_payload.getvalue()
                selected_type = PAYLOAD_TYPE_BINARY

            st.write(f"Raw Payload Footprint: **{len(payload_bytes)} bytes**")

            enc_passphrase = st.text_input(
                "Encryption Passphrase",
                type="password",
                key="enc_pass",
                help="Derived via Scrypt (N=16384, r=8, p=1). Never stored or cached.",
            )

            if st.button("Encrypt & Embed", type="primary"):
                if not payload_bytes:
                    st.error("Payload cannot be empty.")
                elif not enc_passphrase:
                    st.error("Passphrase is required.")
                else:
                    with st.spinner("Executing compression, key derivation, AES-256-GCM, and LSB embedding..."):
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

                            st.success("Embedding succeeded. Ciphertext bound via AEAD.")
                            st.download_button(
                                label="Download Stego Image (PNG)",
                                data=stego_bytes,
                                file_name="stego_vault_output.png",
                                mime="image/png",
                            )
                        except InsufficientCapacityError as err:
                            st.error(f"Capacity exceeded: {err}")
                        except StegoVaultError as err:
                            st.error(f"Encoding halted safely: {err}")
        except Exception as e:
            st.error("Failed to process carrier image safely.")

# ----------------------------------------------------------------------
# 2. DECODE TAB
# ----------------------------------------------------------------------
with tab_decode:
    st.header("Extract & Decrypt Payload")
    stego_file = st.file_uploader(
        "Upload Stego Image (PNG, BMP)",
        type=["png", "bmp"],
        key="dec_stego",
    )

    if stego_file:
        try:
            stego_img = Image.open(stego_file)
            st.image(stego_img, caption="Stego Image Preview", width=300)

            dec_passphrase = st.text_input(
                "Decryption Passphrase",
                type="password",
                key="dec_pass",
            )

            if st.button("Extract & Decrypt", type="primary"):
                if not dec_passphrase:
                    st.error("Passphrase is required.")
                else:
                    with st.spinner("Extracting wire frame, verifying AEAD integrity, and decrypting..."):
                        try:
                            recovered_payload, payload_type = decode_payload(
                                stego_image=stego_img,
                                passphrase=dec_passphrase,
                            )

                            st.success("Integrity verified: Authentication tag and AAD match.")
                            if payload_type == PAYLOAD_TYPE_TEXT:
                                try:
                                    text_result = recovered_payload.decode("utf-8")
                                    st.text_area("Decrypted Plaintext", value=text_result, height=150)
                                except UnicodeDecodeError:
                                    st.warning("Payload marked as text but contains non-UTF-8 bytes.")
                                    st.download_button(
                                        "Download Recovered Raw Data",
                                        data=recovered_payload,
                                        file_name="recovered_payload.bin",
                                    )
                            else:
                                st.download_button(
                                    label="Download Recovered File",
                                    data=recovered_payload,
                                    file_name="recovered_file.bin",
                                    mime="application/octet-stream",
                                )
                        except AuthenticationError:
                            st.error("Authentication failed: Incorrect passphrase or carrier data tampered.")
                        except CorruptPayloadError:
                            st.error("Carrier does not contain a valid StegoVault payload framing envelope.")
                        except InvalidPayloadError as err:
                            st.error(f"Payload validation failure: {err}")
                        except StegoVaultError as err:
                            st.error(f"Extraction failed safely: {err}")
        except Exception:
            st.error("Failed to read image buffer.")

# ----------------------------------------------------------------------
# 3. IMAGE QUALITY TAB
# ----------------------------------------------------------------------
with tab_quality:
    st.header("Image Fidelity Assessment")
    st.write("Calculate perceptual and mathematical differences between original and stego carriers.")

    col1, col2 = st.columns(2)
    with col1:
        img_orig_file = st.file_uploader("Original Carrier", type=["png", "bmp"], key="q_orig")
    with col2:
        img_mod_file = st.file_uploader("Stego Carrier", type=["png", "bmp"], key="q_mod")

    if img_orig_file and img_mod_file:
        try:
            im1 = Image.open(img_orig_file)
            im2 = Image.open(img_mod_file)

            if im1.size != im2.size:
                st.error("Images must possess identical dimensions for comparative fidelity analysis.")
            else:
                mse_val = calculate_mse(im1, im2)
                psnr_val = calculate_psnr(im1, im2)

                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("Image Resolution", f"{im1.width}x{im1.height}")
                m_col2.metric("Mean Squared Error (MSE)", f"{mse_val:.6f}")
                m_col3.metric(
                    "Peak SNR (PSNR)",
                    "∞ dB" if psnr_val == float("inf") else f"{psnr_val:.2f} dB",
                )

                if psnr_val == float("inf"):
                    st.info("The two images are bit-for-bit identical.")
                elif psnr_val >= 50.0:
                    st.success("High fidelity (PSNR >= 50 dB): Imperceptible modifications.")
                else:
                    st.warning("Noticeable degradation (PSNR < 50 dB): Embedding footprint is substantial.")
        except Exception as e:
            st.error(f"Analysis aborted: {e}")

# ----------------------------------------------------------------------
# 4. STEGANALYSIS TAB
# ----------------------------------------------------------------------
with tab_steganalysis:
    st.header("Steganalysis & Visual Inspection")
    st.write("Inspect bit planes and run statistical distribution attacks across pixel pairs.")

    inspect_file = st.file_uploader("Select Image to Inspect", type=["png", "bmp"], key="steg_inspect")

    if inspect_file:
        try:
            target_img = Image.open(inspect_file)
            st.image(target_img, caption="Selected Image", width=300)

            st.subheader("1. LSB Bit-Plane Slicing")
            plane_channel = st.selectbox("Target Channel", ["Red", "Green", "Blue"])
            channel_map = {"Red": 0, "Green": 1, "Blue": 2}

            plane_img = extract_lsb_plane(target_img, channel_map[plane_channel])
            st.image(plane_img, caption=f"Bit-0 Plane for {plane_channel} Channel", use_container_width=True)

            st.subheader("2. Chi-Square Statistical Test")
            p_val, chi_stat = chi_square_attack(target_img)

            st.write(f"**Chi-Square Statistic:** `{chi_stat:.4f}`")
            st.write(f"**Calculated p-value:** `{p_val:.6e}`")

            if p_val < 0.05:
                st.error(
                    "Statistical Anomaly Detected (p < 0.05): "
                    "Adjacent Pairs-of-Values (PoV) display unnatural equalization, "
                    "indicating probable sequential LSB embedding."
                )
            else:
                st.success(
                    "No Structural Bias Detected (p >= 0.05): "
                    "Bit transitions align with natural carrier entropy."
                )

            st.caption(
                "Disclaimer: Statistical analysis evaluates probability, not certainty. "
                "High-entropy source images, noise, and encryption can affect variance."
            )
        except Exception as e:
            st.error(f"Steganalysis failed: {e}")