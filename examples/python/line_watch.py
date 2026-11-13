"""Watch the most picked lines in a league and report what moved since the last run.

    python line_watch.py NBA

The first run saves the 50 most picked lines to line_watch.json. Each later run re-reads
those lines in one /projections-by-ids call, prints every line whose number, line type or
status changed and every line that came off the board, then saves a fresh watchlist from
/trending-projections. Two calls per run, so it fits a cron job or a scheduled GitHub Action.
"""

import json
import os
import sys
from datetime import datetime, timezone

from client import get, label

league = sys.argv[1] if len(sys.argv) > 1 else "NBA"
path = "line_watch.json"
saved = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
watch = saved.get(league, {})

if watch:
    # 1. Re-read the saved lines. Up to 200 ids per call; ids that are no longer on the
    #    board are simply missing from the answer.
    ids = list(watch)[:200]
    now = {row["id"]: row for row in get("/projections-by-ids", ids=",".join(ids))}
    print(f"Since {saved['_saved_at'][:16]} UTC, {len(ids)} watched lines:\n")
    moved = gone = 0
    for pid in ids:
        before, row = watch[pid], now.get(pid)
        if row is None:
            gone += 1
            print(f"  off the board  {before['label']}")
            continue
        changes = [
            f"{field} {before[field]} -> {row[field]}"
            for field in ("line_score", "odds_type", "status")
            if before[field] != row[field]
        ]
        if changes:
            moved += 1
            print(f"  changed        {label(row)}  ({'; '.join(changes)})")
    print(f"\n{moved} changed, {gone} off the board, {len(ids) - moved - gone} unchanged")
else:
    print(f"No watchlist for {league} yet: saving one.")

# 2. A fresh watchlist: the 50 most picked lines right now.
trending = get("/trending-projections", league=league, per_page=50)["projections"]
saved[league] = {
    row["id"]: {
        "label": label(row),
        "line_score": row["line_score"],
        "odds_type": row["odds_type"],
        "status": row["status"],
        "trending_count": row["trending_count"],
    }
    for row in trending
}
saved["_saved_at"] = datetime.now(timezone.utc).isoformat()
json.dump(saved, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\nSaved {len(trending)} lines to {path}. Top 5 by picks:")
for row in trending[:5]:
    print(f"  {row['trending_count']:>6}  {label(row)}")
