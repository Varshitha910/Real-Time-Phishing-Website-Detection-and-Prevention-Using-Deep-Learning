"""Tests for starter URL feature extraction."""

from backend.utils.feature_extractor import extract_url_features


def test_extract_url_features_flags_ip_address() -> None:
    """IP-based URLs should be detected as a risk signal."""

    features = extract_url_features("http://192.168.1.10/login")
    assert features["has_ip_address"] is True
    assert features["uses_https"] is False


def test_extract_url_features_counts_suspicious_keywords() -> None:
    """Phishing-related words should increase the keyword count."""

    features = extract_url_features("https://example.com/secure/account/verify")
    assert features["suspicious_keyword_count"] >= 3

