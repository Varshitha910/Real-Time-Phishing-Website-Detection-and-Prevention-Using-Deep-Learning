"""Domain-level feature extraction.

Future versions can add WHOIS age, DNS validity, registrar information, and
top-level-domain reputation. The starter function keeps offline development
simple and deterministic.
"""

import re
from urllib.parse import urlparse


def extract_domain_features(url: str) -> dict[str, int | bool]:
    """Extract hostname and subdomain risk indicators."""

    hostname = urlparse(url).hostname or ""
    return {
        "domain_length": len(hostname),
        "subdomain_count": max(len(hostname.split(".")) - 2, 0),
        "has_ip_address": bool(re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", hostname)),
    }

