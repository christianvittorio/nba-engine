"""One-off probe: structure of ESPN's keyless DraftKings propBets endpoint for an NBA game."""
import json, urllib.request
def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r: return json.loads(r.read().decode())
    except Exception as ex: return {"_error": f"{type(ex).__name__}: {ex}"}
eid = "401909946"
js = get(f"https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/events/{eid}/competitions/{eid}/odds/100/propBets?lang=en&region=us&limit=200")
items = js.get("items") or []
for it in items[:2]: print(json.dumps(it, indent=1)[:2500])
print("\nkeys of an item:", sorted(items[0].keys()))
ath = items[0]["athlete"]["$ref"]; a = get(ath); print("athlete:", a.get("displayName"), a.get("id"), a.get("fullName"), (a.get("team") or {}).get("$ref"))
import collections
print("types:", collections.Counter(i["type"]["name"] for i in items if i["type"]["id"] in "123456"))
