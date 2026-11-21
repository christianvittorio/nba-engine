"""Run the independent GPT challenger. No writes to the existing engine.

python -m gpt_engine.run --date 2026-11-21
python -m gpt_engine.run                  # today and tomorrow, US Eastern
"""
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import sqlite3
import sys
from zoneinfo import ZoneInfo

from .model import VERSION, build_model, evaluate_saved, load_games
from .compare import compare

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "gpt_engine" / "artifacts"
LOG = OUT / "forecast_log.jsonl"
REPORTS = OUT / "reports"
NY = ZoneInfo("America/New_York")


def as_utc(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


def existing_forecasts() -> dict[tuple[int, int], dict]:
    forecasts = {}
    if not LOG.exists():
        return forecasts
    for line in LOG.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        key = (int(item["season"]), int(item["game_id"]))
        if key in forecasts:
            raise ValueError(f"Duplicate GPT forecast in immutable log: {key}")
        forecasts[key] = item
    return forecasts


def legacy_forecasts() -> dict[tuple[int, int], dict]:
    """Read Claude-era baseline only for display, never as a GPT model feature."""
    path = ROOT / "nba_engine" / "artifacts" / "live.sqlite"
    if not path.exists():
        return {}
    con = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        return {(int(season), int(gid)): {
                    "season": int(season), "game_id": int(gid),
                    "p_home": float(p), "mean_home": float(h), "mean_away": float(a),
                    "mean_margin": float(h - a), "mean_total": float(t),
                    "made_at_utc": made, "tip_utc": (json.loads(details or "{}")).get("tip_utc")}
                for season, gid, p, h, a, t, made, details in con.execute(
                    "SELECT season,game_id,p_home,mean_home,mean_away,mean_total,"
                    "made_at_utc,details_json FROM forecasts "
                    "WHERE model_name='sim_mc' AND mean_total IS NOT NULL")}
    finally:
        con.close()


def markdown_report(day: str, forecasts: list[dict], legacy: dict, metrics: dict,
                    available_games: int, late_games: int, head_to_head: dict | None = None) -> str:
    lines = [f"# GPT challenger forecasts — {day}", "",
             f"Model: {VERSION}. **Independent baseline** using historic game results; "
             "it does not use Claude's ratings, simulation outputs or player predictions.",
             "Source: completed games in the shared SQLite archives; upcoming schedule from ESPN's unofficial feed.",
             "Each new forecast is saved only before its game starts and is never replaced.",
             "No player predictions or betting edges are claimed by this first release.", "",
             f"Found {available_games} scheduled games; skipped {late_games} already tipped-off games; "
             f"GPT pregame forecasts for this date: {len(forecasts)}.", ""]
    if forecasts:
        lines += ["| Game | GPT predicted score | GPT win probability | GPT total | Claude predicted score | Claude win probability |",
                  "|---|---:|---:|---:|---:|---:|"]
        for x in sorted(forecasts, key=lambda g: g["tip_utc"]):
            c = legacy.get((x["season"], x["game_id"]))
            claude_score = f'{c["mean_away"]:.0f}-{c["mean_home"]:.0f}' if c else "—"
            claude_win = f'{c["p_home"]:.1%}' if c else "—"
            lines.append(f'| {x["away"]} @ {x["home"]} | '
                         f'{x["mean_away"]:.0f}-{x["mean_home"]:.0f} | '
                         f'{x["p_home"]:.1%} home | {x["mean_total"]:.1f} | '
                         f'{claude_score} | {claude_win} home |')
    else:
        lines.append("**No valid pregame GPT forecasts for this date.** We do not reuse earlier slates.")
    lines += ["", "## GPT performance on completed, timestamp-validated forecasts", ""]
    if metrics["n"] == 0:
        lines.append("No graded pregame forecasts yet. This is a new challenger; historical results are not retroactively treated as live forecasts.")
    else:
        lines += [f'- Graded games: {metrics["n"]}',
                  f'- Win Brier score: {metrics["brier"]:.4f}',
                  f'- Win log-loss: {metrics["log_loss"]:.4f}',
                  f'- Winner accuracy: {metrics["winner"]:.1%}',
                  f'- Margin MAE: {metrics["margin_mae"]:.2f} points',
                  f'- Total MAE: {metrics["total_mae"]:.2f} points']
    if head_to_head and head_to_head["gpt"]["n"]:
        ours, theirs = head_to_head["gpt"], head_to_head["claude"]
        lines += ["", "## Fair head-to-head on matched completed games", "",
                  f'Matched games (both forecasts pre-tip): {ours["n"]}', "",
                  "| Metric | GPT challenger | Claude existing |",
                  "|---|---:|---:|",
                  f'| Win log-loss (lower better) | {ours["log_loss"]:.4f} | {theirs["log_loss"]:.4f} |',
                  f'| Winner accuracy | {ours["winner"]:.1%} | {theirs["winner"]:.1%} |',
                  f'| Margin MAE (lower better) | {ours["margin_mae"]:.2f} | {theirs["margin_mae"]:.2f} |',
                  f'| Total MAE (lower better) | {ours["total_mae"]:.2f} | {theirs["total_mae"]:.2f} |']
    else:
        lines += ["", "## Fair head-to-head", "",
                  "No matched completed games with both forecasts confirmed before tip-off yet."]
    lines += ["", "For a fair head-to-head, compare the same completed games, forecast lead times, "
              "and consistent pregame injury/lineup information. This report is informational, not a betting recommendation.", ""]
    return "\n".join(lines)


def fetch_upcoming(day: str):
    """Use the already-existing ESPN feed as a data adapter, not Claude's model."""
    sys.path.insert(0, str(ROOT / "nba_engine"))
    from nbaengine.feed import EspnFeed
    feed = EspnFeed(pause_s=0.3)
    _, games = feed.scoreboard(day.replace("-", ""))
    return [game for game in games if game.date == day]


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="US Eastern game date; default today and tomorrow")
    args = parser.parse_args(argv)
    days = [date.fromisoformat(args.date).isoformat()] if args.date else [
        str(datetime.now(NY).date() + timedelta(days=i)) for i in (0, 1)]
    OUT.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    games = load_games()
    legacy = legacy_forecasts()
    saved = existing_forecasts()

    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    new = []
    report_data = []
    for day in days:
        found = fetch_upcoming(day)
        late = 0
        model = None
        for game in sorted(found, key=lambda g: g.tip_utc):
            key = (int(game.season), int(game.game_id))
            if key in saved:
                continue
            tip = as_utc(game.tip_utc)
            if now >= tip:
                late += 1
                continue
            if model is None:
                model = build_model(games, int(game.season), day)
            pred = model.predict(game.home, game.away)
            row = {"model_version": VERSION, "made_at_utc": stamp,
                   "season": int(game.season), "game_id": int(game.game_id),
                   "date": day, "tip_utc": tip.strftime("%Y-%m-%dT%H:%M:%SZ"),
                   "home": game.home, "away": game.away, **pred}
            new.append(row)
            saved[key] = row
        report_data.append((day, len(found), late))

    # Append only: immutable predictions are not replaced on a repeated run.
    if new:
        with LOG.open("a", encoding="utf-8") as f:
            for row in new:
                f.write(json.dumps(row, sort_keys=True) + "\n")
    metrics = evaluate_saved(list(saved.values()), games)
    matched = compare(list(saved.values()), legacy, games)
    for day, n, late in report_data:
        dated = [r for r in saved.values() if r["date"] == day]
        path = REPORTS / f"gpt_forecasts_{day}.md"
        path.write_text(markdown_report(day, dated, legacy, metrics, n, late, matched), encoding="utf-8")
        print(f"GPT {day}: {len(dated)} saved pregame forecasts, {n} upcoming, {late} late; report {path}")
    (OUT / "scorecard.json").write_text(json.dumps(
        {"generated_utc": stamp, "model_version": VERSION, **metrics,
         "head_to_head": matched}, indent=2) + "\n",
        encoding="utf-8")
    print("GPT graded scorecard:", metrics)


if __name__ == "__main__":
    main()
