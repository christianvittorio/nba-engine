"""Prevent accidental sportsbook raw data publication by scheduled CI."""
from pathlib import Path


def test_public_repo_market_workflow_is_ephemeral_and_key_optional():
    root=Path(__file__).resolve().parents[3]
    workflow=(root/".github/workflows/gpt-v2-daily-report.yml"
              ).read_text(encoding="utf-8")
    assert 'HOOPSAPI_KEY: ${{ secrets.HOOPSAPI_KEY }}' not in workflow
    assert "secrets." not in workflow
    assert "python -m gpt_engine.v2.public_espn_odds" in workflow
    assert 'ODDS_API_IO_KEY: ${{ secrets.ODDS_API_IO_KEY }}' not in workflow
    assert 'THE_ODDS_API_KEY: ${{ secrets.THE_ODDS_API_KEY }}' not in workflow
    assert 'python -m gpt_engine.v2.hoopsapi_free' not in workflow
    assert '--ledger /tmp/gpt-v2-odds-log.jsonl' in workflow
    assert '--odds-ledger /tmp/gpt-v2-odds-log.jsonl' in workflow
    assert 'git add -f gpt_engine/v2/artifacts/market/' not in workflow
    assert '--output-json /tmp/gpt-v2-market-asof-latest.json' in workflow
    assert "NO ACCOUNT, NO KEY" in workflow


def test_free_board_is_selected_for_daily_runs():
    root=Path(__file__).resolve().parents[3]
    workflow=(root/".github/workflows/gpt-v2-daily-report.yml").read_text()
    assert '--book-set observed' in workflow
    assert '--output-md /tmp/gpt-v2-five-book-board.md' in workflow
