from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pytest

from itg_sync import ConnectionMetadataStore, GraphSyncJob, get_cursor_snapshot
from itg_sync.sync import FetchCursors, FetchResult, GraphDataSource


@dataclass
class _Dataset:
    inbox: list[str]
    timeline: list[str]


class StubGraph(GraphDataSource):
    def __init__(self, dataset: _Dataset, page_size: int = 2) -> None:
        self.dataset = dataset
        self.page_size = page_size
        self.last_inbox_after: Optional[str] = None
        self.last_timeline_after: Optional[str] = None

    def fetch_inbox(self, *, after: Optional[str]) -> FetchResult:
        self.last_inbox_after = after
        items, next_token = self._page(self.dataset.inbox, after, stream="inbox")
        return FetchResult(items=items, cursors=FetchCursors(after=next_token, next=next_token))

    def fetch_timeline(self, *, after: Optional[str]) -> FetchResult:
        self.last_timeline_after = after
        items, next_token = self._page(self.dataset.timeline, after, stream="timeline")
        return FetchResult(items=items, cursors=FetchCursors(after=next_token, next=next_token))

    def _page(self, data: list[str], after: Optional[str], stream: str) -> tuple[list[str], Optional[str]]:
        start_index = 0
        if after:
            _, _, index = after.partition(":")
            start_index = int(index)
        items = data[start_index : start_index + self.page_size]
        if not items:
            return [], None
        next_index = start_index + len(items)
        next_token = f"{stream}:{next_index}"
        return items, next_token


def _create_store(tmp_path: Path) -> ConnectionMetadataStore:
    return ConnectionMetadataStore(tmp_path / "connection_metadata.json")


def _load_raw(path: Path) -> dict:
    return json.loads(path.read_text("utf-8"))


def test_tokens_are_saved_and_reused(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    store = _create_store(tmp_path)
    dataset = _Dataset(
        inbox=["i1", "i2", "i3"],
        timeline=["t1", "t2", "t3"],
    )
    api = StubGraph(dataset)
    job = GraphSyncJob(api, store)

    caplog.set_level(logging.INFO)

    job.run_pull_sync()

    raw = _load_raw(store.path)  # type: ignore[attr-defined]
    assert raw["cursors"]["inbox"]["next"] == "inbox:2"
    assert raw["cursors"]["timeline"]["next"] == "timeline:2"
    # ensure cursors logged for diagnostics visibility
    assert any("Graph cursors updated" in message for message in caplog.messages)

    diag = get_cursor_snapshot(store)
    assert diag["streams"]["inbox"]["next"] == "inbox:2"

    # Run again and make sure the stored cursor is fed back to the API
    job.run_pull_sync()
    assert api.last_inbox_after == "inbox:2"
    assert api.last_timeline_after == "timeline:2"


def test_sync_resumes_without_duplication(tmp_path: Path) -> None:
    store = _create_store(tmp_path)
    dataset = _Dataset(
        inbox=["i1", "i2", "i3", "i4"],
        timeline=["t1", "t2", "t3", "t4"],
    )
    api = StubGraph(dataset)
    job = GraphSyncJob(api, store)

    first = job.run_pull_sync()
    second = job.run_pull_sync()

    assert list(first.inbox.items) == ["i1", "i2"]
    assert list(second.inbox.items) == ["i3", "i4"]
    assert list(first.timeline.items) == ["t1", "t2"]
    assert list(second.timeline.items) == ["t3", "t4"]

    # Ensure we advanced the cursor after the second pass
    raw = _load_raw(store.path)  # type: ignore[attr-defined]
    assert raw["cursors"]["inbox"]["next"] == "inbox:4"
    assert raw["cursors"]["timeline"]["next"] == "timeline:4"
