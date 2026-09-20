"""
StegoVault - Complete Automated Live Screenshot Capture Utility
Captures high-resolution, pixel-perfect authentic screenshots of all 4 tabs:
1. Main Dashboard & Specifications Overview
2. Secure Encode Workflow (configured + success)
3. Authenticated Decode Workflow (success + auth failure)
4. Image Quality & Perceptual Fidelity (MSE + PSNR)
5. Forensic Steganalysis (LSB Bit-0 Plane Decomposition + Chi-Square Attack)
"""

import sys
import time
from pathlib import Path
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

SCREENSHOTS_DIR = BASE_DIR / "docs" / "screenshots"
RAW_DIR = SCREENSHOTS_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
SCRATCH_DIR = BASE_DIR / "scratch"
SCRATCH_DIR.mkdir(parents=True, exist_ok=True)


def prepare_test_assets():
    carrier_path = SCRATCH_DIR / "carrier_sample.png"
    # Create 600x400 rich carrier image
    img = Image.new("RGB", (600, 400), color=(24, 32, 47))
    draw = ImageDraw.Draw(img)
    for i in range(400):
        r = int(20 + 80 * (i / 400.0))
        g = int(35 + 100 * (i / 400.0))
        b = int(70 + 120 * (i / 400.0))
        draw.line([(0, i), (600, i)], fill=(r, g, b))
    draw.ellipse([150, 80, 450, 320], outline=(100, 180, 255), width=4)
    draw.text((210, 190), "STEGOVAULT CARRIER", fill=(255, 255, 255))
    img.save(carrier_path, "PNG")

    from core.encoder import encode_payload
    from core.payload import PAYLOAD_TYPE_TEXT
    secret = "StegoVault Mission: Secure operational transmission verified by Vivek Rathod. High-entropy defense-in-depth architecture.".encode("utf-8")
    stego_img = encode_payload(img, secret, "SecurePassphrase@2026", PAYLOAD_TYPE_TEXT)
    stego_path = SCRATCH_DIR / "stego_sample.png"
    stego_img.save(stego_path, "PNG")

    return str(carrier_path), str(stego_path)


def capture_all():
    carrier_file, stego_file = prepare_test_assets()
    print("Prepared test carrier and stego assets.")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
            headless=True
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1.5
        )
        page = context.new_page()

        print("1. Opening http://localhost:8505...")
        page.goto("http://localhost:8505", wait_until="networkidle")
        page.wait_for_timeout(2500)

        # Screenshot 1: Main Dashboard Overview
        print("Capturing 01_dashboard_overview.png...")
        page.screenshot(path=str(RAW_DIR / "01_dashboard_overview.png"))

        # Setup Tab 0: Secure Encode
        print("Configuring Tab 0: Secure Encode...")
        # Upload carrier to tab 0
        file_inputs = page.locator('input[type="file"]')
        file_inputs.nth(0).set_input_files(carrier_file)
        page.wait_for_timeout(2000)

        text_area = page.locator('textarea')
        text_area.fill("StegoVault Mission: Secure operational transmission verified by Vivek Rathod. High-entropy defense-in-depth architecture.")
        page.wait_for_timeout(1000)

        pass_inputs = page.locator('input[type="password"]')
        pass_inputs.nth(0).fill("CyberSecurity@2026")
        page.wait_for_timeout(1000)

        # Screenshot 2: Encode Configured
        print("Capturing 02_encode_configured.png...")
        page.screenshot(path=str(RAW_DIR / "02_encode_configured.png"))

        # Click Encrypt & Embed
        page.locator('button:has-text("Encrypt & Embed into Carrier")').click()
        page.wait_for_timeout(3500)

        # Screenshot 3: Encode Success
        print("Capturing 03_encode_success.png...")
        page.screenshot(path=str(RAW_DIR / "03_encode_success.png"))

        # Switch to Tab 1: Authenticated Decode
        print("Switching to Tab 1: Authenticated Decode...")
        tabs = page.locator('[role="tab"]')
        tabs.nth(1).click()
        page.wait_for_timeout(2000)

        # On Tab 1, upload stego carrier
        # Find the file input on Tab 1
        decode_uploader = page.locator('div[data-testid="stFileUploader"] input[type="file"]').nth(1)
        decode_uploader.set_input_files(stego_file)
        page.wait_for_timeout(2000)

        # Enter decryption password
        dec_pass = page.locator('input[type="password"]').nth(1)
        dec_pass.fill("SecurePassphrase@2026")
        page.wait_for_timeout(1000)

        # Click Authenticate & Decrypt
        page.locator('button:has-text("Authenticate & Decrypt")').click()
        page.wait_for_timeout(3000)

        # Screenshot 4: Decode Success
        print("Capturing 04_decode_success.png...")
        page.screenshot(path=str(RAW_DIR / "04_decode_success.png"))

        # Test failure: wrong password
        print("Testing authentication failure...")
        dec_pass.fill("WrongPassword@999")
        page.locator('button:has-text("Authenticate & Decrypt")').click()
        page.wait_for_timeout(2500)

        # Screenshot 5: Decode Auth Failure
        print("Capturing 05_decode_auth_failure.png...")
        page.screenshot(path=str(RAW_DIR / "05_decode_auth_failure.png"))

        # Switch to Tab 2: Image Quality & Fidelity
        print("Switching to Tab 2: Image Quality & Fidelity...")
        tabs.nth(2).click()
        page.wait_for_timeout(2000)

        # Upload original and stego
        q_uploaders = page.locator('div[data-testid="stFileUploader"] input[type="file"]')
        q_uploaders.nth(2).set_input_files(carrier_file)
        page.wait_for_timeout(2000)
        q_uploaders.nth(3).set_input_files(stego_file)
        page.wait_for_timeout(3500)

        # Screenshot 6: Image Quality
        print("Capturing 06_image_quality_fidelity.png...")
        page.screenshot(path=str(RAW_DIR / "06_image_quality_fidelity.png"))

        # Switch to Tab 3: Forensic Steganalysis
        print("Switching to Tab 3: Forensic Steganalysis...")
        tabs.nth(3).click()
        page.wait_for_timeout(2000)

        steg_uploader = page.locator('div[data-testid="stFileUploader"] input[type="file"]').nth(4)
        steg_uploader.set_input_files(stego_file)
        page.wait_for_timeout(3500)

        # Screenshot 7: Steganalysis
        print("Capturing 07_forensic_steganalysis.png...")
        page.screenshot(path=str(RAW_DIR / "07_forensic_steganalysis.png"))

        # Scroll down to capture Chi-Square attack section
        print("Capturing 08_steganalysis_chi_square.png...")
        page.locator('h5:has-text("Pairs of Values")').scroll_into_view_if_needed()
        page.wait_for_timeout(2000)
        page.screenshot(path=str(RAW_DIR / "08_steganalysis_chi_square.png"))

        browser.close()
        print("All raw screenshots successfully captured!")


if __name__ == "__main__":
    capture_all()
