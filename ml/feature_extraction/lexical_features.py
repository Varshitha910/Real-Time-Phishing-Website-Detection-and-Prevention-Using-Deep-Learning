"""Lexical feature extraction from raw URL strings."""

import math
import re
from collections import Counter


SUSPICIOUS_KEYWORDS = {"login", "verify", "update", "secure", "account", "bank", "password", "confirm"}


def extract_lexical_features(url: str) -> dict[str, int | float | bool]:
    """Extract fast lexical features used by both training and inference."""

    return {
        "url_length": len(url),
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "special_char_count": len(re.findall(r"[^A-Za-z0-9]", url)),
        "has_at_symbol": "@" in url,
        "suspicious_keyword_count": sum(1 for word in SUSPICIOUS_KEYWORDS if word in url.lower()),
        "url_entropy": round(_shannon_entropy(url), 4),
    }


def _shannon_entropy(value: str) -> float:
    """Calculate character entropy to flag random-looking URLs."""

    if not value:
        return 0.0
    counts = Counter(value)
    length = len(value)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())

