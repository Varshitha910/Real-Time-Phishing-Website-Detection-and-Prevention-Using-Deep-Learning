"""Security header defaults for future middleware integration."""


SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
}


def get_security_headers() -> dict[str, str]:
    """Return a copy of recommended security headers."""

    return SECURITY_HEADERS.copy()

