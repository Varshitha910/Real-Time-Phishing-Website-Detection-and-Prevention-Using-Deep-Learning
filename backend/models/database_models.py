"""Database model helpers for MongoDB documents.

These functions keep document shapes consistent before a dedicated ODM is
introduced.
"""

from datetime import datetime, timezone
from typing import Any


def build_scan_document(scan_result: dict[str, Any]) -> dict[str, Any]:
    """Build a MongoDB-ready scan document from an API result."""

    return {
        **scan_result,
        "created_at": datetime.now(datetime.now(timezone.utc)),
        "updated_at": datetime.now(datetime.now(timezone.utc)),
    }

