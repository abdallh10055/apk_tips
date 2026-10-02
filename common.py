import json, os, datetime
BASE = os.path.dirname(os.path.abspath(__file__))
STORE = os.environ.get("ANDROID_PRIVATE", BASE)
PREFS = os.path.join(STORE, "prefs.json")

def load_tips():
    with open(os.path.join(BASE, "tips_data.json"), encoding="utf-8") as f:
        return json.load(f)

def load_prefs():
    d = {"start": str(datetime.date.today()), "hour": 9, "minute": 0,
         "enabled": True, "done": [], "last_notified": ""}
    try:
        with open(PREFS, encoding="utf-8") as f:
            d.update(json.load(f))
    except Exception:
        pass
    return d

def update_prefs(**kw):
    d = load_prefs(); d.update(kw)
    with open(PREFS, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)
    return d

def today_index(p, n):
    return (datetime.date.today() - datetime.date.fromisoformat(p["start"])).days % n
