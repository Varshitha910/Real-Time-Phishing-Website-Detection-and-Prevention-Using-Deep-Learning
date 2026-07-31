"""HTML content feature extraction placeholders.

Content features inspect page markup for forms, iframes, external scripts, and
credential collection patterns. This starter accepts optional HTML text so it
can be tested without making network requests.
"""

from bs4 import BeautifulSoup


def extract_content_features(html: str | None = None) -> dict[str, int | float | bool]:
    """Extract basic HTML signals from supplied page content."""

    if not html:
        return {
            "form_count": 0,
            "iframe_count": 0,
            "script_count": 0,
            "has_password_input": False,
        }

    soup = BeautifulSoup(html, "html.parser")
    return {
        "form_count": len(soup.find_all("form")),
        "iframe_count": len(soup.find_all("iframe")),
        "script_count": len(soup.find_all("script")),
        "has_password_input": soup.find("input", {"type": "password"}) is not None,
    }

