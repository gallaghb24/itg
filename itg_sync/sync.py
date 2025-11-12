"""Sync job capable of seeding Graph fetches from stored cursors."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, Optional, Protocol

from .storage import ConnectionMetadataStore, CursorPayload


@dataclass(frozen=True)
class FetchCursors:
    """Cursors returned by a single Graph fetch."""

    after: Optional[str]
    next: Optional[str]


@dataclass(frozen=True)
class FetchResult:
    items: Iterable[object]
    cursors: FetchCursors


@dataclass(frozen=True)
class SyncResult:
    inbox: FetchResult
    timeline: FetchResult


class GraphDataSource(Protocol):
    """Minimal protocol for the Graph client used by the sync job."""

    def fetch_inbox(self, *, after: Optional[str]) -> FetchResult:
        ...

    def fetch_timeline(self, *, after: Optional[str]) -> FetchResult:
        ...


class GraphSyncJob:
    """Coordinates Graph pulls while persisting paging cursors."""

    def __init__(
        self,
        api: GraphDataSource,
        store: ConnectionMetadataStore,
        *,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.api = api
        self.store = store
        self.logger = logger or logging.getLogger(__name__)

    def run_pull_sync(self, *, use_stored_cursors: bool = True) -> SyncResult:
        """Run a pull sync, optionally seeding Graph with stored paging cursors."""

        seeds = self.store.get_cursors() if use_stored_cursors else {}
        inbox_seed = seeds.get("inbox", {}).get("next")
        timeline_seed = seeds.get("timeline", {}).get("next")

        inbox_result = self.api.fetch_inbox(after=inbox_seed)
        timeline_result = self.api.fetch_timeline(after=timeline_seed)

        self._persist({
            "inbox": inbox_result.cursors,
            "timeline": timeline_result.cursors,
        })

        self._log_cursors(inbox_result.cursors, timeline_result.cursors)

        return SyncResult(inbox=inbox_result, timeline=timeline_result)

    # Internal helpers -------------------------------------------------
    def _persist(self, updates: dict[str, FetchCursors]) -> None:
        payload: dict[str, CursorPayload] = {}
        for stream, cursors in updates.items():
            payload[stream] = {"after": cursors.after, "next": cursors.next}
        self.store.record_batch(payload)

    def _log_cursors(self, inbox: FetchCursors, timeline: FetchCursors) -> None:
        self.logger.info(
            "Graph cursors updated",
            extra={
                "graph_cursors": {
                    "inbox": {"after": inbox.after, "next": inbox.next},
                    "timeline": {"after": timeline.after, "next": timeline.next},
                }
            },
        )
