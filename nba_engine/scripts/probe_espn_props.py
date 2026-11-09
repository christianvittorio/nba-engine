"""One-off probe: does ESPN expose player-prop lines for an NBA game without a key? Prints what the odds endpoints contain."""
import json, sys, urllib.request
def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r: return json.loads(r.read().decode())
    except Exception as ex: return {"_error": f"{type(ex).__name__}: {ex}"}
sb = get("https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard")
ev = (sb.get("events") or [{}])[0]; eid = ev.get("id"); print("event", eid, ev.get("name"))
def keys(o, depth=0, path=""):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            out.append(path + "/" + k); 
            if depth < 4: out += keys(v, depth + 1, path + "/" + k)
    elif isinstance(o, list) and o and depth < 4: out += keys(o[0], depth + 1, path + "[]")
    return out
hits = []
for name, u in (("summary", f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={eid}"),
                ("core odds", f"https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/events/{eid}/competitions/{eid}/odds"),
                ("core providers", "https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/providers?limit=100")):
    js = get(u); ks = keys(js); pk = [k for k in ks if any(w in k.lower() for w in ("prop", "player", "athlete"))]
    print(f"\n== {name}: {len(ks)} keys; error={js.get('_error')}; prop/player-like keys: {pk[:15]}")
    if name == "core odds":
        for it in (js.get("items") or [])[:4]:
            print("  provider", (it.get("provider") or {}).get("name"), "| top keys", sorted(it.keys())[:25])
            for k, v in it.items():
                if isinstance(v, dict) and "$ref" in v: print("   ref", k, v["$ref"][:140])
