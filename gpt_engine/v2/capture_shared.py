"""Archive only timestamped ESPN observations already produced by Claude.

This is a raw-data sharing workflow. It does NOT copy Claude's forecasts,
injury model coefficients, lineup guesses or player probability outputs.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
from pathlib import Path
import json
from .contracts import iso
from .shared_availability import capture_snapshot,CLAUDE_SNAPSHOT,ARCHIVE

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--source",default=str(CLAUDE_SNAPSHOT))
    p.add_argument("--output-folder",default=str(ARCHIVE))
    p.add_argument("--max-age-hours",type=float,default=12)
    a=p.parse_args(argv)
    original=json.loads(Path(a.source).read_text(encoding="utf-8"))
    if len(original.get("teams") or {})<28:
        raise ValueError("Refuse partial ESPN league collection (<28 team rosters)")
    path=capture_snapshot(a.source,folder=a.output_folder,
                          max_age_hours=a.max_age_hours)
    snap=json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps({
        "saved":str(path),
        "generated_utc":snap["generated_utc"],
        "team_count":len(snap["teams"]),
        "injury_count":sum(len(x.get("injuries",[])) for x in snap["teams"].values()),
        "unresolved_id_count":snap["unresolved_id_count"],
        "has_confirmed_starters":False,
        "uses_claude_model_outputs":False,
    },indent=2))

if __name__=="__main__":
    main()
