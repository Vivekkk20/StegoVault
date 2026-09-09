"""
Integration Tests: REST API Endpoints
"""
import io
from PIL import Image


def test_health_check_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app_name"] == "StegoVault"
    assert "security" in data


def test_capacity_endpoint(client, sample_png_bytes):
    response = client.post(
        "/api/v1/steganography/capacity",
        files={"file": ("cover.png", sample_png_bytes, "image/png")},
        data={"message": "Testing capacity endpoint"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["capacity_bytes"] > 0
    assert data["sufficient_capacity"] is True


def test_encode_and_decode_api_roundtrip(client, sample_png_bytes):
    # 1. Encode
    secret = "Top secret payload for API integration test"
    password = "IntegrationPassword2026!"

    encode_res = client.post(
        "/api/v1/steganography/encode",
        files={"file": ("test_cover.png", sample_png_bytes, "image/png")},
        data={
            "secret_message": secret,
            "password": password,
            "confirm_password": password,
            "output_filename": "encoded_test.png",
        }
    )
    assert encode_res.status_code == 200
    enc_data = encode_res.json()
    assert enc_data["success"] is True
    download_url = enc_data["download_url"]

    # 2. Download stego image
    dl_res = client.get(download_url)
    assert dl_res.status_code == 200
    stego_bytes = dl_res.content

    # 3. Detect payload
    detect_res = client.post(
        "/api/v1/steganography/detect",
        files={"file": ("stego.png", stego_bytes, "image/png")}
    )
    assert detect_res.status_code == 200
    assert detect_res.json()["detected"] is True

    # 4. Decode
    decode_res = client.post(
        "/api/v1/steganography/decode",
        files={"file": ("stego.png", stego_bytes, "image/png")},
        data={"password": password}
    )
    assert decode_res.status_code == 200
    dec_data = decode_res.json()
    assert dec_data["secret_message"] == secret
    assert dec_data["integrity_verified"] is True

    # 5. Decode with wrong password fails with 401
    bad_decode = client.post(
        "/api/v1/steganography/decode",
        files={"file": ("stego.png", stego_bytes, "image/png")},
        data={"password": "WrongPassword!"}
    )
    assert bad_decode.status_code == 401


def test_analyzer_and_reports_api(client, sample_png_bytes):
    # 1. Analyze image
    analyze_res = client.post(
        "/api/v1/analyzer/analyze",
        files={"file": ("sample.png", sample_png_bytes, "image/png")}
    )
    assert analyze_res.status_code == 200
    report = analyze_res.json()
    assert "analysis_id" in report
    analysis_id = report["analysis_id"]
    assert "section_1_file_information" in report
    assert "section_10_risk_score" in report

    # 2. List reports
    reports_res = client.get("/api/v1/reports")
    assert reports_res.status_code == 200
    reports_list = reports_res.json()
    assert any(r["analysis_id"] == analysis_id for r in reports_list)

    # 3. Get single report
    single_res = client.get(f"/api/v1/reports/{analysis_id}")
    assert single_res.status_code == 200
    assert single_res.json()["analysis_id"] == analysis_id

    # 4. Export report HTML
    export_html_res = client.get(f"/api/v1/reports/{analysis_id}/export?format=html")
    assert export_html_res.status_code == 200
    assert "StegoVault Forensic Security Report" in export_html_res.text

    # 5. Export report JSON
    export_json_res = client.get(f"/api/v1/reports/{analysis_id}/export?format=json")
    assert export_json_res.status_code == 200
    assert export_json_res.json()["analysis_id"] == analysis_id
