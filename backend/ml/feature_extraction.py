# """URL feature extraction used by backend inference and training."""

# from __future__ import annotations

# import math
# import re
# from collections import Counter
# from urllib.parse import urlparse


# FEATURE_COLUMNS = [
#     "url_length",
#     "domain_length",
#     "path_length",
#     "dot_count",
#     "special_char_count",
#     "https_available",
#     "ip_address_present",
#     "suspicious_word_count",
#     "url_entropy",
#     "subdomain_count",
#     "hyphen_count",
# ]

# SUSPICIOUS_WORDS = {
#     "account",
#     "bank",
#     "confirm",
#     "free",
#     "login",
#     "password",
#     "paypal",
#     "secure",
#     "security",
#     "update",
#     "verify",
#     "wallet",
# }

# IP_PATTERN = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
# SPECIAL_PATTERN = re.compile(r"[^A-Za-z0-9]")


# def extract_url_features(url: str) -> dict[str, float | int]:
#     """Extract numerical phishing indicators from a URL."""

#     normalized = sanitize_url(url)
#     parsed = urlparse(normalized)
#     host = parsed.hostname or ""
#     path = parsed.path or ""

#     return {
#         "url_length": len(normalized),
#         "domain_length": len(host),
#         "path_length": len(path),
#         "dot_count": normalized.count("."),
#         "special_char_count": len(SPECIAL_PATTERN.findall(normalized)),
#         "https_available": int(parsed.scheme == "https"),
#         "ip_address_present": int(_is_ip_address(host)),
#         "suspicious_word_count": sum(1 for word in SUSPICIOUS_WORDS if word in normalized.lower()),
#         "url_entropy": round(_entropy(normalized), 6),
#         "subdomain_count": max(len([part for part in host.split(".") if part]) - 2, 0),
#     }


# def feature_vector(url: str) -> list[float]:
#     """Return a model-ready vector in stable feature order."""

#     features = extract_url_features(url)
#     return [float(features[column]) for column in FEATURE_COLUMNS]


# def sanitize_url(url: str) -> str:
#     """Trim and normalize a URL before validation and feature extraction."""

#     cleaned = str(url).strip()
#     if not cleaned:
#         raise ValueError("URL cannot be empty.")
#     if cleaned.startswith(("http://", "https://")):
#         return cleaned
#     return f"http://{cleaned}"


# def _is_ip_address(host: str) -> bool:
#     """Detect valid IPv4 hostnames."""

#     if not IP_PATTERN.fullmatch(host):
#         return False
#     return all(0 <= int(part) <= 255 for part in host.split("."))


# def _entropy(value: str) -> float:
#     """Calculate Shannon entropy for randomness detection."""

#     if not value:
#         return 0.0
#     counts = Counter(value)
#     length = len(value)
#     return -sum((count / length) * math.log2(count / length) for count in counts.values())

"""URL feature extraction used by backend inference and training."""

from __future__ import annotations

import math
import re
from collections import Counter
from urllib.parse import urlparse


# MUST MATCH scaler.pkl training features (11 features)
FEATURE_COLUMNS = [
    "url_length",
    "domain_length",
    "path_length",
    "dot_count",
    "special_char_count",
    "https_available",
    "ip_address_present",
    "suspicious_word_count",
    "url_entropy",
    "subdomain_count",
    "hyphen_count",
]


SUSPICIOUS_WORDS = {
    "account",
    "bank",
    "confirm",
    "free",
    "login",
    "password",
    "paypal",
    "secure",
    "security",
    "update",
    "verify",
    "wallet",
}


IP_PATTERN = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")

SPECIAL_PATTERN = re.compile(
    r"[^A-Za-z0-9]"
)


def extract_url_features(url: str) -> dict[str, float | int]:
    """
    Extract numerical phishing indicators from a URL.
    """

    normalized = sanitize_url(url)

    parsed = urlparse(normalized)

    host = parsed.hostname or ""

    path = parsed.path or ""


    return {

        # 1
        "url_length": len(normalized),

        # 2
        "domain_length": len(host),

        # 3
        "path_length": len(path),

        # 4
        "dot_count": normalized.count("."),

        # 5
        "special_char_count": len(
            SPECIAL_PATTERN.findall(normalized)
        ),

        # 6
        "https_available": int(
            parsed.scheme == "https"
        ),

        # 7
        "ip_address_present": int(
            _is_ip_address(host)
        ),

        # 8
        "suspicious_word_count": sum(
            1 for word in SUSPICIOUS_WORDS
            if word in normalized.lower()
        ),

        # 9
        "url_entropy": round(
            _entropy(normalized),
            6
        ),

        # 10
        "subdomain_count": max(
            len(
                [
                    part
                    for part in host.split(".")
                    if part
                ]
            ) - 2,
            0
        ),

        # 11 (added to match scaler)
        "hyphen_count": normalized.count("-"),
    }



def feature_vector(url: str) -> list[float]:
    """
    Return model-ready feature vector.
    Order MUST match FEATURE_COLUMNS.
    """

    features = extract_url_features(url)

    return [
        float(features[column])
        for column in FEATURE_COLUMNS
    ]



def sanitize_url(url: str) -> str:
    """
    Normalize URL.
    """

    cleaned = str(url).strip()

    if not cleaned:
        raise ValueError(
            "URL cannot be empty."
        )

    if cleaned.startswith(
        ("http://", "https://")
    ):
        return cleaned

    return "http://" + cleaned



def _is_ip_address(host: str) -> bool:
    """
    Detect IPv4 address.
    """

    if not IP_PATTERN.fullmatch(host):
        return False


    return all(
        0 <= int(part) <= 255
        for part in host.split(".")
    )



def _entropy(value: str) -> float:
    """
    Shannon entropy calculation.
    """

    if not value:
        return 0.0


    counts = Counter(value)

    length = len(value)


    return -sum(
        (count / length)
        * math.log2(count / length)

        for count in counts.values()
    )