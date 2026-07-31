"""Network feature extraction placeholders.

These features may require live HTTP, DNS, or SSL checks, so the starter keeps
the interface stable while avoiding network calls during early development.
"""


def extract_network_features(url: str) -> dict[str, int | float | bool]:
    """Return default network features until live checks are enabled."""

    return {
        "redirect_count": 0,
        "http_status_code": 0,
        "response_time_ms": 0.0,
        "has_valid_ssl": url.startswith("https://"),
    }

