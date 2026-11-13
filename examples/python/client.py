"""Minimal client for the PrizePicks API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os

import requests

HOST = "prizepicks-api.p.rapidapi.com"


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, **params):
    """GET an endpoint and return the `data` part of the response (an object or a list)."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    if not body.get("success", True):
        raise RuntimeError(f"{path} failed: {body}")
    return body["data"]


def label(row):
    """One line of text for a projection: player, stat, line, line type and opponent.

    `description` holds the opponent's abbreviation on player lines, and `odds_type` says
    whether the number is the standard line, an easier goblin or a harder demon line, so two
    lines on the same player and stat are not duplicates.
    """
    player = row["player"]
    return (
        f"{player['name']} ({player['team']}) {row['stat_type']} {row['line_score']} "
        f"[{row['odds_type']}] vs {row['description']}"
    )


def tipoff(row):
    """`start_time` carries the US Eastern offset (-05:00 or -04:00). Returns 'YYYY-MM-DD HH:MM ET'."""
    return row["start_time"][:16].replace("T", " ") + " ET"
