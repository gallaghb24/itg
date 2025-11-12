"""Diagnostics helpers for exposing persisted cursors."""

from __future__ import annotations

from typing import Dict

from .storage import ConnectionMetadataStore


def get_cursor_snapshot(store: ConnectionMetadataStore) -> Dict[str, Dict[str, object]]:
    """Return the cursor payload in a diagnostics-friendly format."""

    cursors = store.get_cursors()
    return {
        "streams": {
            name: {"after": payload.get("after"), "next": payload.get("next")}
            for name, payload in cursors.items()
        }
    }
