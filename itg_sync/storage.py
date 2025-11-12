"""Persistent storage helpers for Graph paging cursors."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Optional

CursorPayload = Dict[str, Optional[str]]


class ConnectionMetadataStore:
    """Small wrapper around the JSON metadata file used by Graph connections."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    # Internal helpers -------------------------------------------------
    def _load_raw(self) -> Dict[str, object]:
        if not self.path.exists():
            return {}
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
                if isinstance(data, dict):
                    return data
        except json.JSONDecodeError:
            # Corrupt or unreadable metadata should not crash syncs; start fresh.
            pass
        return {}

    def _write_raw(self, payload: Dict[str, object]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)

    # Public API -------------------------------------------------------
    def get_cursors(self) -> Dict[str, CursorPayload]:
        raw = self._load_raw()
        cursors = raw.get("cursors", {}) if isinstance(raw, dict) else {}
        if not isinstance(cursors, dict):
            return {}
        # Defensive copy so callers cannot mutate internal state.
        return {
            stream: {
                "after": values.get("after"),
                "next": values.get("next"),
            }
            for stream, values in cursors.items()
            if isinstance(values, dict)
        }

    def update_cursor(
        self,
        stream: str,
        *,
        after: Optional[str],
        next_token: Optional[str],
    ) -> None:
        raw = self._load_raw()
        if not isinstance(raw, dict):
            raw = {}
        cursors = raw.setdefault("cursors", {})
        if not isinstance(cursors, dict):
            cursors = {}
            raw["cursors"] = cursors
        cursors[stream] = {"after": after, "next": next_token}
        self._write_raw(raw)

    def seed_for(self, stream: str) -> Optional[str]:
        return self.get_cursors().get(stream, {}).get("next")

    def record_batch(self, updates: Dict[str, CursorPayload]) -> None:
        for stream, payload in updates.items():
            self.update_cursor(
                stream,
                after=payload.get("after"),
                next_token=payload.get("next"),
            )
