import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
import arabic_reshaper
from bidi.algorithm import get_display
from common import load_tips, load_prefs, update_prefs, today_index

FONTS = ["/system/fonts/NotoNaskhArabic-Regular.ttf", "/system/fonts/NotoSansArabic-Regular.ttf",
         "/system/fonts/DroidSansArabic.ttf", "C:/Windows/Fonts/arial.ttf"]
FONT = next((f for f in FONTS if os.path.exists(f)), None)

def fix(t): return get_display(arabic_reshaper.reshape(t))

def L(text, size=20, h=None):
    l = Label(text=fix(text), font_size=size, halign="right", valign="middle",
              size_hint_y=None, height=h or size * 6, font_name=FONT or "Roboto")
    l.bind(width=lambda w, v: setattr(w, "text_size", (v - 20, None)))
    return l

class TipsApp(App):
    def build(self):
        self.tips = load_tips()
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions(["android.permission.POST_NOTIFICATIONS"])
            from android import AndroidService
            AndroidService("نصائح", "تعمل في الخلفية").start("run")
        self.root_box = BoxLayout(orientation="vertical", padding=10, spacing=8)
        self.render(); return self.root_box

    def render(self):
        b = self.root_box; b.clear_widgets()
        p = load_prefs(); i = today_index(p, len(self.tips)); t = self.tips[i]
        b.add_widget(L(f"اليوم {i + 1} من {len(self.tips)}", 22, 50))
        sv = ScrollView(); inner = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        inner.bind(minimum_height=inner.setter("height"))
        inner.add_widget(L("نصيحة التغذية", 24, 50))
        inner.add_widget(L(t["nutrition_tip"], 20, 200))
        inner.add_widget(L("التمرين الخفي", 24, 50))
        inner.add_widget(L(t["invisible_exercise"], 20, 220))
        sv.add_widget(inner); b.add_widget(sv)
        done = str(i) in map(str, p["done"])
        btn = Button(text=fix("✔ تم" if done else "تم التنفيذ"), size_hint_y=None, height=60,
                     font_name=FONT or "Roboto")
        btn.bind(on_release=lambda *_: self.mark(i)); b.add_widget(btn)
        row = BoxLayout(size_hint_y=None, height=60, spacing=6)
        for txt, fn in [("الساعة +", lambda: self.shift(1)), ("الساعة -", lambda: self.shift(-1)),
                        ("تشغيل/إيقاف", self.toggle)]:
            x = Button(text=fix(txt), font_name=FONT or "Roboto")
            x.bind(on_release=lambda _, f=fn: f()); row.add_widget(x)
        b.add_widget(row)
        b.add_widget(L(f"التنبيه: {p['hour']:02d}:{p['minute']:02d} — {'مفعل' if p['enabled'] else 'متوقف'}", 18, 40))

    def mark(self, i):
        p = load_prefs(); s = set(map(str, p["done"])); s.add(str(i))
        update_prefs(done=sorted(s)); self.render()
    def shift(self, d):
        update_prefs(hour=(load_prefs()["hour"] + d) % 24); self.render()
    def toggle(self):
        update_prefs(enabled=not load_prefs()["enabled"]); self.render()

TipsApp().run()
