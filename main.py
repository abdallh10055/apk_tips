import os, sys, time, datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import load_tips, load_prefs, update_prefs, today_index
from plyer import notification
import arabic_reshaper
from bidi.algorithm import get_display

def fix(t): return get_display(arabic_reshaper.reshape(t))

while True:
    try:
        p = load_prefs(); now = datetime.datetime.now(); today = str(now.date())
        due = (now.hour, now.minute) >= (p["hour"], p["minute"])
        if p["enabled"] and due and p["last_notified"] != today:
            tips = load_tips(); t = tips[today_index(p, len(tips))]
            notification.notify(title=fix("نصيحة اليوم"),
                message=fix(t["nutrition_tip"] + "\n" + t["invisible_exercise"]),
                app_name="Tips", timeout=60)
            update_prefs(last_notified=today)
    except Exception:
        pass
    time.sleep(30)
