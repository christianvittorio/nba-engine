"""Prevent accidental sportsbook raw data publication by scheduled CI."""
from pathlib import Path


def test_public_repo_market_workflow_is_ephemeral_and_key_optional():
    root=Path(__file__).resolve().parents[3]
    workflow=(root/".github/workflows/gpt-v2-daily-report.yml"
              ).read_text(encoding="utf-8")
    assert 'THE_ODDS_API_KEY: ${{ secrets.THE_ODDS_API_KEY }}' in workflow
    assert '--ledger /tmp/gpt-v2-odds-log.jsonl' in workflow
    assert '--odds-ledger /tmp/gpt-v2-odds-log.jsonl' in workflow
    assert 'git add -f gpt_engine/v2/artifacts/market/' not in workflow
    assert '--output-json /tmp/gpt-v2-market-asof-latest.json' in workflow
    assert "No configured odds API secret; skip live feed" in workflow
