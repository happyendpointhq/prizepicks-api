"""The most picked lines on one league's board, then every line posted on the top player.

    python quickstart.py NBA
"""

import sys
from collections import defaultdict

from client import get, label, tipoff

league = sys.argv[1] if len(sys.argv) > 1 else "NBA"

# 1. The whole board, most picked first. Read each row's start_time: the board is posted
#    ahead, and today_only=true follows the platform's own sports day, so on the afternoon
#    before a slate it returned 0 of 1,482 NBA lines.
board = get(
    "/projections",
    league=league,
    sort="trending_count",
    sort_direction="desc",
    per_page=25,
)
rows = board["projections"]
print(f"{board['pagination']['total']} {league} lines on the board, showing {len(rows)}\n")
for row in rows[:10]:
    print(f"{tipoff(row)}  {row['trending_count'] or 0:>6} picks  {label(row)}")

if not rows:
    raise SystemExit("No lines on this board. Try another league from /leagues.")

# 2. Every line on the most picked player. One player often has a standard line and easier
#    (goblin) or harder (demon) lines on the same stat.
player = rows[0]["player"]
lines = get("/player-projections", league=league, player_id=player["id"], per_page=200)["projections"]
by_stat = defaultdict(list)
for row in lines:
    by_stat[row["stat_type"]].append(f"{row['line_score']} {row['odds_type']}")
print(f"\n{player['name']}: {len(lines)} lines")
for stat, values in sorted(by_stat.items()):
    print(f"  {stat:<22} {', '.join(values)}")
