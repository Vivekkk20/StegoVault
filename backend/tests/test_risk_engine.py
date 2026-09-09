"""
Unit Tests: Forensic Risk Scoring Engine
"""
from app.steganalysis.risk_engine import calculate_risk_score


def test_clean_image_low_risk():
    structure = {"trailing_data": {"detected": False}, "metadata": {}}
    entropy = {"is_lsb_anomaly": False, "suspicious_channels": []}
    lsb = {"suspicious_channels_count": 0, "summary": "Normal"}
    histogram = {"is_flattened_anomaly": False, "pov_pairing_delta": {}}
    correlation = {"is_correlation_anomaly": False, "lsb_plane_correlation": {}}

    res = calculate_risk_score(structure, entropy, lsb, histogram, correlation)
    assert res["score"] <= 20
    assert res["risk_level"] == "VERY_LOW"
    assert "limitations" in res


def test_stegovault_detected_critical_risk():
    structure = {"trailing_data": {"detected": False}, "metadata": {}}
    entropy = {"is_lsb_anomaly": False, "suspicious_channels": []}
    lsb = {"suspicious_channels_count": 0, "summary": "Normal"}
    histogram = {"is_flattened_anomaly": False}
    correlation = {"is_correlation_anomaly": False}
    stegovault = {
        "detected": True,
        "version": 1,
        "total_payload_bytes": 500,
        "header_crc_valid": True,
        "ciphertext_length": 408,
    }

    res = calculate_risk_score(
        structure, entropy, lsb, histogram, correlation, stegovault_detection=stegovault
    )
    assert res["score"] >= 80
    assert res["risk_level"] in ("HIGH", "CRITICAL")
    assert any("StegoVault" in ind["name"] for ind in res["indicators"])


def test_trailing_data_adds_significant_risk():
    structure = {
        "trailing_data": {
            "detected": True,
            "trailing_size_bytes": 1024,
            "sha256": "abc12345",
            "legal_eof_offset": 5000,
        },
        "metadata": {}
    }
    entropy = {"is_lsb_anomaly": False}
    lsb = {"suspicious_channels_count": 0}
    histogram = {"is_flattened_anomaly": False}
    correlation = {"is_correlation_anomaly": False}

    res = calculate_risk_score(structure, entropy, lsb, histogram, correlation)
    assert res["score"] >= 35
    assert any("Trailing" in ind["name"] for ind in res["indicators"])
