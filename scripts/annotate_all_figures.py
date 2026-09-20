"""
StegoVault - Master High-Resolution Screenshot Annotation Generator
Produces all 8 annotated publication-grade figures with pixel-perfect alignment
matching the 2520x1680 live Playwright captures.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "docs" / "screenshots" / "raw"
OUT_DIR = BASE_DIR / "docs" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def draw_cursor(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 2.0):
    """Draws a crisp modern pointer cursor at (x, y)."""
    pts = [
        (0, 0),
        (0, int(22 * scale)),
        (int(5 * scale), int(17 * scale)),
        (int(10 * scale), int(27 * scale)),
        (int(14 * scale), int(25 * scale)),
        (int(9 * scale), int(15 * scale)),
        (int(16 * scale), int(15 * scale)),
    ]
    abs_pts = [(x + px, y + py) for px, py in pts]
    shadow_pts = [(px + 4, py + 4) for px, py in abs_pts]
    draw.polygon(shadow_pts, fill=(0, 0, 0, 160))
    draw.polygon(abs_pts, fill=(255, 255, 255, 255), outline=(15, 23, 42, 255), width=2)


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color=(220, 38, 38, 255), width=6):
    """Draws a directional arrow from start to end with an arrowhead at end."""
    x0, y0 = start
    x1, y1 = end
    draw.line([start, end], fill=color, width=width)
    angle = math.atan2(y1 - y0, x1 - x0)
    arrow_len = 32
    arrow_angle = math.pi / 6
    p1 = (x1 - arrow_len * math.cos(angle - arrow_angle), y1 - arrow_len * math.sin(angle - arrow_angle))
    p2 = (x1 - arrow_len * math.cos(angle + arrow_angle), y1 - arrow_len * math.sin(angle + arrow_angle))
    draw.polygon([(x1, y1), p1, p2], fill=color)


def draw_badge(draw: ImageDraw.ImageDraw, x: int, y: int, number: int, bg_color=(239, 68, 68, 255), size=48):
    """Draws a numbered circle badge with clear centered text."""
    draw.ellipse([x - size // 2, y - size // 2, x + size // 2, y + size // 2], fill=bg_color, outline=(255, 255, 255, 255), width=4)
    try:
        font = ImageFont.truetype("arialbd.ttf", 26)
    except Exception:
        font = ImageFont.load_default()
    draw.text((x, y), str(number), fill=(255, 255, 255, 255), font=font, anchor="mm")


def annotate_all():
    # -------------------------------------------------------------
    # Fig 1: Dashboard Overview
    # -------------------------------------------------------------
    im1 = Image.open(RAW_DIR / "01_dashboard_overview.png").convert("RGBA")
    ov1 = Image.new("RGBA", im1.size, (0, 0, 0, 0))
    d1 = ImageDraw.Draw(ov1)

    # 1: Mode Switch Tabs
    d1.rounded_rectangle([750, 550, 2160, 645], radius=16, outline=(2, 132, 199, 255), width=5)
    draw_badge(d1, 750, 550, 1, bg_color=(2, 132, 199, 255))
    draw_cursor(d1, 890, 600)

    # 2: Sidebar Cryptographic Engine
    d1.rounded_rectangle([25, 500, 575, 1260], radius=16, outline=(147, 51, 234, 255), width=5)
    draw_badge(d1, 575, 500, 2, bg_color=(147, 51, 234, 255))

    # 3: StegoVault Header & Architecture Pills
    d1.rounded_rectangle([750, 210, 2180, 515], radius=16, outline=(22, 163, 74, 255), width=5)
    draw_badge(d1, 2180, 210, 3, bg_color=(22, 163, 74, 255))

    Image.alpha_composite(im1, ov1).convert("RGB").save(OUT_DIR / "fig01_dashboard_overview.png", "PNG")
    print("Fig 1 generated.")

    # -------------------------------------------------------------
    # Fig 2: Encode Configured
    # -------------------------------------------------------------
    im2 = Image.open(RAW_DIR / "02_encode_configured.png").convert("RGBA")
    ov2 = Image.new("RGBA", im2.size, (0, 0, 0, 0))
    d2 = ImageDraw.Draw(ov2)

    # 1: Carrier Ingestion Uploader & Preview
    d2.rounded_rectangle([740, 480, 1530, 1650], radius=16, outline=(2, 132, 199, 255), width=5)
    draw_badge(d2, 740, 480, 1, bg_color=(2, 132, 199, 255))

    # 2: Secret Payload Input & Byte Budget Meter
    d2.rounded_rectangle([1570, 480, 2360, 1510], radius=16, outline=(22, 163, 74, 255), width=5)
    draw_badge(d2, 1570, 480, 2, bg_color=(22, 163, 74, 255))

    # 3: Encryption Passphrase Input
    d2.rounded_rectangle([1570, 1530, 2360, 1675], radius=14, outline=(217, 119, 6, 255), width=5)
    draw_badge(d2, 2360, 1530, 3, bg_color=(217, 119, 6, 255))
    draw_cursor(d2, 1950, 1600)

    Image.alpha_composite(im2, ov2).convert("RGB").save(OUT_DIR / "fig02_encode_configured.png", "PNG")
    print("Fig 2 generated.")

    # -------------------------------------------------------------
    # Fig 3: Encode Success
    # -------------------------------------------------------------
    im3 = Image.open(RAW_DIR / "03_encode_success.png").convert("RGBA")
    ov3 = Image.new("RGBA", im3.size, (0, 0, 0, 0))
    d3 = ImageDraw.Draw(ov3)

    # 1: Success Alert Banner (bound to AAD header)
    d3.rounded_rectangle([1590, 1385, 2360, 1555], radius=16, outline=(22, 163, 74, 255), width=5)
    draw_badge(d3, 1590, 1385, 1, bg_color=(22, 163, 74, 255))

    # 2: One-Click Stego Carrier Download Button
    d3.rounded_rectangle([1590, 1575, 2360, 1655], radius=16, outline=(2, 132, 199, 255), width=5)
    draw_badge(d3, 2360, 1575, 2, bg_color=(2, 132, 199, 255))
    draw_cursor(d3, 1975, 1615)

    Image.alpha_composite(im3, ov3).convert("RGB").save(OUT_DIR / "fig03_encode_success.png", "PNG")
    print("Fig 3 generated.")

    # -------------------------------------------------------------
    # Fig 4: Decode Success
    # -------------------------------------------------------------
    im4 = Image.open(RAW_DIR / "04_decode_success.png").convert("RGBA")
    ov4 = Image.new("RGBA", im4.size, (0, 0, 0, 0))
    d4 = ImageDraw.Draw(ov4)

    # 1: Authenticated Integrity Status Badge
    d4.rounded_rectangle([1590, 1250, 2360, 1420], radius=16, outline=(22, 163, 74, 255), width=5)
    draw_badge(d4, 1590, 1250, 1, bg_color=(22, 163, 74, 255))

    # 2: Recovered Plaintext Hash Match Box
    d4.rounded_rectangle([1590, 1450, 2360, 1565], radius=14, outline=(2, 132, 199, 255), width=5)
    draw_badge(d4, 2360, 1450, 2, bg_color=(2, 132, 199, 255))

    # 3: Passphrase & Authenticate Button
    d4.rounded_rectangle([1590, 970, 2360, 1225], radius=14, outline=(147, 51, 234, 255), width=5)
    draw_badge(d4, 1590, 970, 3, bg_color=(147, 51, 234, 255))
    draw_cursor(d4, 1970, 1180)

    Image.alpha_composite(im4, ov4).convert("RGB").save(OUT_DIR / "fig04_decode_success.png", "PNG")
    print("Fig 4 generated.")

    # -------------------------------------------------------------
    # Fig 5: Decode Auth Failure (Tamper Defense)
    # -------------------------------------------------------------
    im5 = Image.open(RAW_DIR / "05_decode_auth_failure.png").convert("RGBA")
    ov5 = Image.new("RGBA", im5.size, (0, 0, 0, 0))
    d5 = ImageDraw.Draw(ov5)

    # 1: Wrong Passphrase Input
    d5.rounded_rectangle([1590, 970, 2360, 1070], radius=14, outline=(217, 119, 6, 255), width=5)
    draw_badge(d5, 1590, 970, 1, bg_color=(217, 119, 6, 255))
    draw_cursor(d5, 1850, 1020)

    # 2: Authentication Rejection Notice (GHASH failure)
    d5.rounded_rectangle([1590, 1250, 2360, 1420], radius=16, outline=(220, 38, 38, 255), width=5)
    draw_badge(d5, 2360, 1250, 2, bg_color=(220, 38, 38, 255))
    draw_arrow(d5, (1970, 1220), (1970, 1250), color=(220, 38, 38, 255), width=6)

    Image.alpha_composite(im5, ov5).convert("RGB").save(OUT_DIR / "fig05_decode_auth_failure.png", "PNG")
    print("Fig 5 generated.")

    # -------------------------------------------------------------
    # Fig 6: Image Quality & Fidelity
    # -------------------------------------------------------------
    im6 = Image.open(RAW_DIR / "06_image_quality_fidelity.png").convert("RGBA")
    ov6 = Image.new("RGBA", im6.size, (0, 0, 0, 0))
    d6 = ImageDraw.Draw(ov6)

    # 1: Dual Image Uploaders
    d6.rounded_rectangle([750, 880, 2360, 1040], radius=14, outline=(2, 132, 199, 255), width=5)
    draw_badge(d6, 750, 880, 1, bg_color=(2, 132, 199, 255))

    # 2: Empirical Quality Metrics (Resolution, MSE, PSNR)
    d6.rounded_rectangle([750, 1140, 2360, 1340], radius=16, outline=(22, 163, 74, 255), width=5)
    draw_badge(d6, 2360, 1140, 2, bg_color=(22, 163, 74, 255))

    # 3: Pristine Fidelity Status Badge
    d6.rounded_rectangle([750, 1360, 2360, 1480], radius=14, outline=(147, 51, 234, 255), width=5)
    draw_badge(d6, 750, 1360, 3, bg_color=(147, 51, 234, 255))
    draw_cursor(d6, 1550, 1420)

    Image.alpha_composite(im6, ov6).convert("RGB").save(OUT_DIR / "fig06_image_quality_fidelity.png", "PNG")
    print("Fig 6 generated.")

    # -------------------------------------------------------------
    # Fig 7: Forensic Steganalysis LSB Plane
    # -------------------------------------------------------------
    im7 = Image.open(RAW_DIR / "07_forensic_steganalysis.png").convert("RGBA")
    ov7 = Image.new("RGBA", im7.size, (0, 0, 0, 0))
    d7 = ImageDraw.Draw(ov7)

    # 1: Carrier Overview
    d7.rounded_rectangle([750, 1220, 1260, 1580], radius=16, outline=(2, 132, 199, 255), width=5)
    draw_badge(d7, 750, 1220, 1, bg_color=(2, 132, 199, 255))

    # 2: Bit-0 Plane Visualization
    d7.rounded_rectangle([1310, 1220, 2360, 1600], radius=16, outline=(220, 38, 38, 255), width=5)
    draw_badge(d7, 2360, 1220, 2, bg_color=(220, 38, 38, 255))
    draw_cursor(d7, 1840, 1440)

    Image.alpha_composite(im7, ov7).convert("RGB").save(OUT_DIR / "fig07_steganalysis_lsb_plane.png", "PNG")
    print("Fig 7 generated.")

    # -------------------------------------------------------------
    # Fig 8: Chi-Square Attack
    # -------------------------------------------------------------
    im8 = Image.open(RAW_DIR / "08_steganalysis_chi_square.png").convert("RGBA")
    ov8 = Image.new("RGBA", im8.size, (0, 0, 0, 0))
    d8 = ImageDraw.Draw(ov8)

    # 1: Chi-Square Statistical Test Metrics
    d8.rounded_rectangle([750, 1000, 2360, 1170], radius=16, outline=(2, 132, 199, 255), width=5)
    draw_badge(d8, 750, 1000, 1, bg_color=(2, 132, 199, 255))
    draw_cursor(d8, 1050, 1085)

    # 2: Statistical Anomaly Alert Banner
    d8.rounded_rectangle([750, 1195, 2360, 1410], radius=16, outline=(220, 38, 38, 255), width=5)
    draw_badge(d8, 2360, 1195, 2, bg_color=(220, 38, 38, 255))
    draw_arrow(d8, (1555, 1470), (1555, 1415), color=(220, 38, 38, 255), width=6)

    Image.alpha_composite(im8, ov8).convert("RGB").save(OUT_DIR / "fig08_steganalysis_chi_square.png", "PNG")
    print("Fig 8 generated.")


if __name__ == "__main__":
    annotate_all()
