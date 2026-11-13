# PrizePicks API and Scraper

The PrizePicks API returns the PrizePicks board as JSON: every player projection (line) for a
league with the stat, the number, whether it is a standard, goblin or demon line, the wager
types it allows, the athlete, team, opponent and game, its start time and status, and how many
entries have picked it. It also returns live, promotional and trending lines, every line on
one player or one game, up to 200 known lines in one call, and the leagues, stat types,
players, teams and games behind each board. It is a REST API, so the lines go straight into
your own code without building and maintaining a PrizePicks scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/prizepicks-api?utm_source=github&utm_medium=readme&utm_campaign=prizepicks-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/prizepicks-api
- Product page: https://happyendpoint.com/library/prizepicks-api?utm_source=github&utm_medium=readme&utm_campaign=prizepicks-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://prizepicks-api.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 17, all `GET` |
| Leagues | Every league on the PrizePicks board; `/leagues` lists them with their live line counts |
| Filters | Player, team, position, stat type, line type, status, game, live, promo, line range, pick count and start time window |
| Page size | `per_page` up to 200 (default 50) |
| Format | JSON, every response wrapped in `{"success": true, "data": ...}` |

---

## What data you get

**Lines (projections)**
- One league's whole board, filtered, sorted (board rank, line, start time, pick count, player, stat, last update) and paged
- Every line on one player, or on one game
- Lines on games already under way, promotional lines with the original number next to the discounted one, and the most picked lines
- One line by id, or up to 200 ids in one call for a watchlist

**Each line carries**
- `line_score`, `stat_type`, `odds_type` (`standard`, `goblin` easier, `demon` harder), `allowed_wager_types`, `status`
- The athlete (name, position, jersey, team), the team, the opponent, the game with both teams, start time and live flags
- `trending_count`: how many entries have picked it

**Leagues and directory**
- Leagues with their live line counts, a league's stat types, its players, teams and games
- A board summary: totals by line type, stat and wager type, the line range and the busiest stat markets

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/prizepicks-api). Current plans are listed there. Copy `.env.example` to `.env` and paste your key.

### 2. Make a request

The 25 most picked NBA lines on the board:

```bash
curl "https://prizepicks-api.p.rapidapi.com/projections?league=NBA&sort=trending_count&sort_direction=desc&per_page=25" \
  -H "x-rapidapi-host: prizepicks-api.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py NBA
```

```python
from client import get, label

board = get("/projections", league="NBA", sort="trending_count",
            sort_direction="desc", per_page=25)
for row in board["projections"]:
    print(row["trending_count"], label(row))
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs NBA
```

---

## Example response

`GET /projections?league=NBA&sort=trending_count&sort_direction=desc&per_page=25`, recorded
on 3 November 2026 (US time) and trimmed to one line and a few fields. More responses are in
[`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "league": { "id": "7", "name": "NBA" },
    "projections": [
      {
        "id": "16579989",
        "line_score": 34.5,
        "stat_type": "Points",
        "description": "SAC",
        "odds_type": "standard",
        "allowed_wager_types": "over",
        "status": "pre_game",
        "trending_count": 28700,
        "start_time": "2026-11-04T22:10:00.000-05:00",
        "today": null,
        "player": { "id": "227710", "name": "Luka Dončić", "position": "F-G", "team": "LAL" },
        "duration": { "id": "11", "name": "Full" }
      }
    ],
    "pagination": { "page": 1, "per_page": 25, "total": 1482, "total_pages": 60, "has_more": true },
    "sort": { "key": "trending_count", "direction": "desc" }
  }
}
```

---

## Endpoints

Base URL: `https://prizepicks-api.p.rapidapi.com`

### Lines

| Endpoint | Returns |
|---|---|
| `GET /projections` | One league's board of lines, with every filter, sort and page option |
| `GET /player-projections` | Every line posted on one player, by id or name |
| `GET /game-projections` | Every line on one game, by either of its ids |
| `GET /live-projections` | Lines on games already under way |
| `GET /promo-projections` | Promotional and discounted lines, with the original number |
| `GET /trending-projections` | The most picked lines, ranked by pick count |
| `GET /projection-details` | One line by id, with athlete, team, league, game and stat resolved |
| `GET /projections-by-ids` | Up to 200 lines by id in one call |

### Leagues

| Endpoint | Returns |
|---|---|
| `GET /leagues` | Every league, with its live line count and filter values |
| `GET /league-details` | One league, with its stat types |
| `GET /stat-types` | The stat types a league's board can be filtered by |
| `GET /board-summary` | A league's board in numbers: totals, breakdowns, line range, busiest stats |

### Directory

| Endpoint | Returns |
|---|---|
| `GET /players` | Athletes on a league's board, with their team and line count |
| `GET /player-details` | One athlete and what they have lines on |
| `GET /teams` | Teams on a league's board, spelled as the team filter expects |
| `GET /games` | Games on a league's board, with start times and live status |
| `GET /status` | Service health |

---

## Things to know about the data

These come from running the examples on 3 November 2026 (US time) against the NBA board for
the games of 4 November. They are the details that give wrong answers rather than errors.

- **One player, one stat, several lines.** Tyrese Maxey's points had a standard line at 23.5,
  a goblin at 19.5 and a demon at 24.5. Group by player, stat and `odds_type`, never by player
  and stat alone. Of the 50 most picked lines, 45 were standard, 3 goblin and 2 demon.
- **Goblin lines are over only.** Every goblin line we saw had `allowed_wager_types: "over"`,
  as did most demons; standard lines were `under_or_over`, `over` or null (22 rows).
- **The board is posted ahead.** Every one of the 1,482 NBA lines started on 4 November, the
  next day in US Eastern time, and `today` was null on all of them, so `today_only=true`
  returned nothing. Use `starts_after` and `starts_before` for a time window.
- **Times are US Eastern.** `start_time` carries the offset (`-05:00`), so convert before you
  compare with UTC.
- **`description` is the opponent.** On player lines it holds the opponent's abbreviation
  (`SAC`, `DET`), not a text description.
- **Trending is a subset.** `/trending-projections` keeps lines with at least one pick: 304 of
  the 1,482. 11 rows across our pulls had `trending_count: null`, which sorts last.
- **Pick counts climb by the minute.** The most picked line went from 28,597 to 28,700 picks
  within minutes. Store the time with every count.
- **`/projections-by-ids` returns a list, not an object.** `data` is an array of lines; ids
  that are off the board are left out rather than returned as errors. `line_watch.py` treats
  a missing id as a line taken down.
- **Ids are strings,** for lines, players, teams and games alike.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | The most picked lines on a league's board, then every line posted on the top player, grouped by stat |
| [`examples/python/line_watch.py`](examples/python/line_watch.py) | Saves the 50 most picked lines, and on each later run reports every line whose number, line type or status changed and every line taken off the board; two calls per run, for a cron job |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | The most picked lines in Node 18+, no dependencies |
| [`samples/`](samples/) | Recorded responses for four endpoints |

---

## API or your own PrizePicks scraper

A homemade PrizePicks scraper has to keep up with the app's internal API, join lines to
players, teams and games itself, and cope with blocks on busy game nights. This API returns
the lines already joined, with the goblin and demon flags and pick counts, as documented JSON,
so the work you keep is your model or your product. If you need a one-off export or a
recurring feed rather than API calls, [contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=prizepicks-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can read the board without
code:

```json
{
  "mcpServers": {
    "prizepicks": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: prizepicks-api.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there a PrizePicks API?

PrizePicks does not publish a public developer API for its board. This API, built and
maintained by Happy Endpoint and independent of PrizePicks, returns the board's lines, players,
teams and games as REST and JSON.

### How do I get PrizePicks lines in Python?

Install `requests`, set `RAPIDAPI_KEY`, and call `/projections` with a league such as `NBA`.
[`examples/python/client.py`](examples/python/client.py) is a short client, and
[`quickstart.py`](examples/python/quickstart.py) prints the most picked lines.

### What are goblin and demon lines?

Alternative lines on the same player and stat: a goblin is set easier than the standard line
and a demon harder. `odds_type` tells them apart, and `/projections?odds_type=demon` filters
to one kind.

### Can I track line movement?

Yes. Save the ids you care about and re-read them with `/projections-by-ids` (up to 200 per
call). [`line_watch.py`](examples/python/line_watch.py) does this and reports what changed.

### Does it include user or account data?

No. The API returns the public board: athletes, teams, games and lines, with pick counts as
totals. It has no endpoints for entries, users or accounts.

### Is there a free PrizePicks API?

Plans, including what each one allows, are on the
[RapidAPI listing](https://rapidapi.com/happyendpoint/api/prizepicks-api), where every endpoint
can also be tested in the browser.

---

## Related repos

- [happyendpoint-python](https://github.com/happyendpointhq/happyendpoint-python) - Python client covering every Happy Endpoint API
- [happyendpoint-mcp](https://github.com/happyendpointhq/happyendpoint-mcp) - MCP server for Claude, Cursor and other assistants
- [happyendpoint-js](https://github.com/happyendpointhq/happyendpoint-js) - TypeScript client
- [awesome-alternative-data](https://github.com/happyendpointhq/awesome-alternative-data) - alternative data sources for research

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: hello@happyendpoint.com

## Licence

MIT. See [LICENSE](LICENSE).
