"""URL validation and normalization helpers."""

from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    """Return True when a URL has a scheme and network location."""

    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def normalize_url(url: str) -> str:
    """Normalize common URL input differences before feature extraction."""

    stripped_url = url.strip()
    if stripped_url.startswith("http://") or stripped_url.startswith("https://"):
        return stripped_url
    return f"https://{stripped_url}"

