# Sample responses

Real `200` responses from four PrizePicks API endpoints, recorded on 3 November 2026 (US
time) while testing the examples, on the NBA board for games on 4 November. Long arrays are
cut to their first three items. The responses hold athletes, teams and lines only: no user
or account data. `group_key` (a compound key of player, stat and game ids) is removed from
each line. Field names and values are otherwise unchanged. File names follow the
endpoint path.

| File | Request |
|---|---|
| `projections.json` | `GET /projections?league=NBA&sort=trending_count&sort_direction=desc&per_page=25` |
| `player-projections.json` | `GET /player-projections?league=NBA&player_id=227710&per_page=200` |
| `trending-projections.json` | `GET /trending-projections?league=NBA&per_page=50` |
| `projections-by-ids.json` | `GET /projections-by-ids?ids=16593344,16593362,16593271` |

The `projections-by-ids.json` call was sent with 50 ids; the file keeps the first three rows.
Lines and pick counts change by the minute, so do not hard-code these values.
