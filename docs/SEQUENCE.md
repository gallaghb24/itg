# Graph Cursor Sequence

1. A pull sync requests stored `next` cursors from the metadata store.
2. The sync job seeds the Graph inbox and timeline fetches with these values.
3. Each fetch returns items and the next cursor token supplied by Graph.
4. The sync job records the `after`/`next` pair back to the metadata store and
   emits a diagnostic log entry.
5. Diagnostics or API consumers can query the metadata store snapshot to expose
   the last seen cursor values.
