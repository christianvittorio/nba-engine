"""One-off probe: structure of ESPN's keyless DraftKings propBets endpoint for an NBA game."""
import json, urllib.request
def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r: return json.loads(r.read().decode())
    except Exception as ex: return {"_error": f"{type(ex).__name__}: {ex}"}
sb = get("https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard")
for ev in (sb.get("events") or [])[:3]:
    eid = ev["id"]; print("\n#### event", eid, ev.get("name"), ev["status"]["type"]["name"])
    js = get(f"https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/events/{eid}/competitions/{eid}/odds/100/propBets?lang=en&region=us&limit=200")
    print("error:", js.get("_error"), "| top keys:", list(js)[:12], "| count", js.get("count"), "pageCount", js.get("pageCount"))
    items = js.get("items") or []
    print("items:", len(items))
    for it in items[:6]: print(json.dumps(it)[:700])
    types = {}
    for it in items: types[json.dumps(it.get("type"))[:80]] = types.get(json.dumps(it.get("type"))[:80], 0) + 1
    print("types:", dict(list(types.items())[:30]))
