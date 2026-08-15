import threading
import time
import socket
import sys
from datetime import date
from typing import List, Dict, Tuple
from PIL import Image, ImageDraw, ImageFont
import pystray
from pystray import MenuItem as item
import tkinter as tk
from tkinter import font as tkfont

# ============================================================
# HYBRID BIKRAM SAMBAT ENGINE
# ============================================================
BS_MONTH_TABLE: Dict[int, List[int]] = {
    1975: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    1976: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    1977: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    1978: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    1979: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    1980: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    1981: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
    1982: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    1983: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    1984: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    1985: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
    1986: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    1987: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    1988: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    1989: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
    1990: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    1991: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
    1992: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    1993: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    1994: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    1995: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
    1996: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    1997: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    1998: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    1999: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2000: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    2001: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2002: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2003: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2004: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    2005: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2006: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2007: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2008: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31],
    2009: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2010: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2011: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2012: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
    2013: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2014: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2015: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2016: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
    2017: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2018: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2019: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    2020: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
    2021: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2022: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
    2023: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    2024: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
    2025: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2026: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2027: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    2028: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2029: [31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30],
    2030: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2031: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    2032: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2033: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2034: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2035: [30, 32, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31],
    2036: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2037: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2038: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2039: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
    2040: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2041: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2042: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2043: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
    2044: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2045: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2046: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2047: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
    2048: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2049: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
    2050: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    2051: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
    2052: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2053: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
    2054: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    2055: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2056: [31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30],
    2057: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2058: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    2059: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2060: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2061: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2062: [31, 31, 31, 32, 31, 31, 29, 30, 29, 30, 29, 31],
    2063: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2064: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2065: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2066: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31],
    2067: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2068: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2069: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2070: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
    2071: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2072: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2073: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    2074: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
    2075: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2076: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
    2077: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    2078: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
    2079: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
    2080: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
    2081: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
    2082: [31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30],
    2083: [31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30],
    2084: [31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30],
    2085: [31, 32, 31, 32, 30, 31, 30, 30, 29, 30, 30, 30],
    2086: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30],
    2087: [31, 31, 32, 31, 31, 31, 30, 29, 30, 30, 30, 30],
    2088: [30, 31, 32, 32, 30, 31, 30, 30, 29, 30, 30, 30],
    2089: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30],
    2090: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30],
    2091: [31, 31, 32, 31, 31, 31, 30, 30, 29, 30, 30, 30],
    2092: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 30, 30],
    2093: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30],
    2094: [31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30],
    2095: [31, 31, 32, 31, 31, 31, 30, 29, 30, 30, 30, 30],
    2096: [30, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
    2097: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30],
    2098: [31, 31, 32, 31, 31, 31, 29, 30, 29, 30, 29, 31],
    2099: [31, 31, 32, 31, 31, 31, 30, 29, 29, 30, 30, 30],
    2100: [31, 32, 31, 32, 30, 31, 30, 29, 30, 29, 30, 30],
}

NEPALI_MONTHS = ["बैशाख", "जेठ", "असार", "श्रावण", "भदौ", "असोज",
                 "कार्तिक", "मंसिर", "पुस", "माघ", "फाल्गुन", "चैत"]
ENGLISH_MONTHS = ["Baisakh", "Jestha", "Ashadh", "Shrawan", "Bhadra", "Ashwin",
                  "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra"]
NEPALI_WEEKDAYS = ["आइत", "सोम", "मंगल", "बुध", "बिहि", "शुक्र", "शनि"]
ENGLISH_WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
NEPALI_DIGITS = "०१२३४५६७८९"

def to_nepali_num(n: int) -> str:
    return "".join(NEPALI_DIGITS[int(d)] for d in str(n))

def approximate_month_lengths(bs_year: int) -> List[int]:
    base = [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30]
    v = (bs_year % 5) - 2
    lengths = base.copy()
    lengths[1] = 31 + (1 if v > 0 else 0)
    lengths[5] = 30 + (1 if v < 0 else 0)
    lengths[8] = 29 + (1 if bs_year % 4 == 0 else 0)
    return [max(29, min(32, d)) for d in lengths]

def get_month_lengths(bs_year: int) -> List[int]:
    return BS_MONTH_TABLE.get(bs_year, approximate_month_lengths(bs_year))

ANCHOR_AD = date(2000, 1, 1)
ANCHOR_BS = (2056, 9, 17)

def ad_to_bs(ad_date: date) -> Tuple[int, int, int]:
    delta = (ad_date - ANCHOR_AD).days
    y, m, d = ANCHOR_BS
    d += delta
    while True:
        dim = get_month_lengths(y)[m - 1]
        if d > dim:
            d -= dim
            m += 1
            if m > 12:
                m = 1
                y += 1
        elif d < 1:
            m -= 1
            if m < 1:
                m = 12
                y -= 1
            d += get_month_lengths(y)[m - 1]
        else:
            break
    return y, m, d

def get_bs_today() -> dict:
    today = date.today()
    y, m, d = ad_to_bs(today)
    weekday = (today.weekday() + 1) % 7
    return {
        "year": y, "month": m, "day": d, "weekday": weekday,
        "month_name_np": NEPALI_MONTHS[m-1],
        "month_name_en": ENGLISH_MONTHS[m-1],
        "weekday_np": NEPALI_WEEKDAYS[weekday],
        "weekday_en": ENGLISH_WEEKDAYS[weekday],
        "days_in_month": get_month_lengths(y)[m-1],
        "is_accurate": y in BS_MONTH_TABLE
    }

# ============================================================
# APP SETTINGS
# ============================================================
USE_NEPALI = True
SHOW_OVERLAY = False
ALWAYS_ON_TOP = True
DRAGGABLE = True
CALENDAR_STAY_OPEN = False
LAST_OVERLAY_X = LAST_OVERLAY_Y = None
overlay_root = None

def is_already_running():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 54321))
        s.listen(1)
        return False, s
    except OSError:
        return True, None

already_running, lock_socket = is_already_running()
if already_running:
    sys.exit(0)

# ============================================================
# OVERLAY
# ============================================================
class DateOverlay:
    def __init__(self):
        global overlay_root
        self.root = tk.Tk()
        overlay_root = self.root
        self.root.overrideredirect(True)
        self.root.configure(bg="#111111")
        self.root.attributes("-alpha", 0.90)
        self.root.attributes("-topmost", ALWAYS_ON_TOP)

        try:
            self.font = tkfont.Font(family="Nirmala UI", size=13, weight="bold")
        except:
            self.font = tkfont.Font(family="Segoe UI", size=13, weight="bold")

        self.label = tk.Label(self.root, text="", font=self.font,
                              fg="white", bg="#111111", padx=16, pady=8)
        self.label.pack()

        self.apply_draggable()
        self.update_date()

        if LAST_OVERLAY_X is not None:
            self.root.geometry(f"+{LAST_OVERLAY_X}+{LAST_OVERLAY_Y}")
        else:
            self.position_window()

        self.root.after(20000, self.schedule_update)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def apply_draggable(self):
        for w in (self.root, self.label):
            w.unbind("<Button-1>")
            w.unbind("<B1-Motion>")
        if DRAGGABLE:
            self.root.bind("<Button-1>", self.start_move)
            self.root.bind("<B1-Motion>", self.do_move)
            self.label.bind("<Button-1>", self.start_move)
            self.label.bind("<B1-Motion>", self.do_move)

    def update_date(self):
        bs = get_bs_today()
        if USE_NEPALI:
            text = f"{bs['month_name_np']} {to_nepali_num(bs['day'])}, {bs['weekday_np']}"
        else:
            text = f"{bs['month_name_en']} {bs['day']}, {bs['weekday_en']}"
        color = "#ff5555" if bs["weekday"] in (0, 6) else "white"
        self.label.config(text=text, fg=color)

    def position_window(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_reqwidth(), self.root.winfo_reqheight()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"+{sw-w-200}+{sh-h-48}")

    def schedule_update(self):
        if self.root.winfo_exists():
            self.update_date()
            self.root.after(20000, self.schedule_update)

    def start_move(self, e):
        self._x, self._y = e.x, e.y

    def do_move(self, e):
        global LAST_OVERLAY_X, LAST_OVERLAY_Y
        x = self.root.winfo_x() + e.x - self._x
        y = self.root.winfo_y() + e.y - self._y
        self.root.geometry(f"+{x}+{y}")
        LAST_OVERLAY_X, LAST_OVERLAY_Y = x, y

    def on_close(self):
        global SHOW_OVERLAY, overlay_root
        SHOW_OVERLAY = False
        overlay_root = None
        self.root.destroy()

def run_overlay():
    DateOverlay()

def close_overlay():
    global overlay_root, SHOW_OVERLAY
    if overlay_root:
        try:
            overlay_root.after(0, overlay_root.destroy)
        except:
            pass
        overlay_root = None
    SHOW_OVERLAY = False

# ============================================================
# CALENDAR
# ============================================================
class NepaliCalendarWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.configure(bg="#1e1e1e")
        self.root.attributes("-topmost", True)

        w, h = 420, 420
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{sw - w - 18}+{sh - h - 50}")

        bs = get_bs_today()
        self.year = bs["year"]
        self.month = bs["month"]
        self._editing_year = False

        self.setup_ui()
        self.draw_calendar()

        self.root.bind("<FocusOut>", self.on_focus_out)
        self.root.focus_force()
        self.root.mainloop()

    def on_focus_out(self, event):
        if self._editing_year or CALENDAR_STAY_OPEN:
            return

        # Delay the check so focus can settle on the Entry
        self.root.after(150, self._check_and_close)

    def _check_and_close(self):
        if self._editing_year or CALENDAR_STAY_OPEN:
            return
        try:
            focused = self.root.focus_get()
            # If focus is still inside this window, do nothing
            if focused is not None:
                return
            self.root.destroy()
        except:
            pass

    def toggle_pin(self):
        global CALENDAR_STAY_OPEN
        CALENDAR_STAY_OPEN = not CALENDAR_STAY_OPEN
        self.btn_pin.config(
            text="📌" if CALENDAR_STAY_OPEN else "📍",
            bg="#0066cc" if CALENDAR_STAY_OPEN else "#333"
        )

    def on_year_focus_in(self, event):
        self._editing_year = True

    def on_year_enter(self, event=None):
        try:
            raw = self.year_var.get().strip()
            for i, d in enumerate(NEPALI_DIGITS):
                raw = raw.replace(d, str(i))
            new_year = int(raw)
            if 1000 <= new_year <= 3000:
                self.year = new_year
                self.draw_calendar()
            else:
                self.year_var.set(to_nepali_num(self.year) if USE_NEPALI else str(self.year))
        except:
            self.year_var.set(to_nepali_num(self.year) if USE_NEPALI else str(self.year))

        self._editing_year = False
        self.root.focus_force()   # return focus to the window

    def setup_ui(self):
        outer = tk.Frame(self.root, bg="#1e1e1e")
        outer.pack(fill="both", expand=True, padx=16, pady=14)

        header = tk.Frame(outer, bg="#1e1e1e")
        header.pack(fill="x", pady=(2, 8))

        tk.Button(header, text="◀", font=("Segoe UI", 12, "bold"),
                  bg="#333", fg="white", relief="flat", width=3,
                  command=self.prev_month, cursor="hand2").pack(side="left")

        center = tk.Frame(header, bg="#1e1e1e")
        center.pack(side="left", expand=True)

        self.lbl_month = tk.Label(center, text="", font=("Nirmala UI", 13, "bold"),
                                  bg="#1e1e1e", fg="white")
        self.lbl_month.pack(side="left", padx=(0, 4))

        self.year_var = tk.StringVar()
        self.year_entry = tk.Entry(
            center,
            textvariable=self.year_var,
            font=("Nirmala UI", 13, "bold"),
            width=5,
            justify="center",
            bg="#2a2a2a",
            fg="white",
            insertbackground="white",
            relief="flat",
            bd=0
        )
        self.year_entry.pack(side="left")
        self.year_entry.bind("<FocusIn>", self.on_year_focus_in)
        self.year_entry.bind("<Return>", self.on_year_enter)
        self.year_entry.bind("<FocusOut>", self.on_year_enter)

        self.btn_pin = tk.Button(header, text="📍", font=("Segoe UI", 11),
                                 bg="#333", fg="white", relief="flat", width=3,
                                 command=self.toggle_pin, cursor="hand2")
        self.btn_pin.pack(side="left", padx=8)

        tk.Button(header, text="▶", font=("Segoe UI", 12, "bold"),
                  bg="#333", fg="white", relief="flat", width=3,
                  command=self.next_month, cursor="hand2").pack(side="right")

        self.grid = tk.Frame(outer, bg="#1e1e1e")
        self.grid.pack()

        weekdays = NEPALI_WEEKDAYS if USE_NEPALI else ENGLISH_WEEKDAYS
        for i, d in enumerate(weekdays):
            color = "#ff5555" if i in (0, 6) else "#bbbbbb"
            tk.Label(self.grid, text=d, width=4,
                     font=("Nirmala UI", 10, "bold"),
                     bg="#1e1e1e", fg=color).grid(row=0, column=i, padx=4, pady=5)

        tk.Button(outer, text="आज" if USE_NEPALI else "Today",
                  font=("Nirmala UI", 10), bg="#444", fg="white",
                  relief="flat", command=self.go_today,
                  cursor="hand2").pack(pady=(16, 4))

    def draw_calendar(self):
        for w in self.grid.winfo_children():
            if int(w.grid_info()["row"]) > 0:
                w.destroy()

        month_name = NEPALI_MONTHS[self.month-1] if USE_NEPALI else ENGLISH_MONTHS[self.month-1]
        self.lbl_month.config(text=month_name)
        self.year_var.set(to_nepali_num(self.year) if USE_NEPALI else str(self.year))

        bs = get_bs_today()
        y, m, d = bs["year"], bs["month"], bs["day"]
        days_diff = 0

        while (y, m) != (self.year, self.month):
            if (y > self.year) or (y == self.year and m > self.month):
                d -= 1
                days_diff -= 1
                if d < 1:
                    m -= 1
                    if m < 1:
                        m = 12
                        y -= 1
                    d = get_month_lengths(y)[m-1]
            else:
                d += 1
                days_diff += 1
                if d > get_month_lengths(y)[m-1]:
                    d = 1
                    m += 1
                    if m > 12:
                        m = 1
                        y += 1

        start_weekday = (bs["weekday"] - (bs["day"] - 1) + days_diff) % 7
        days_in_month = get_month_lengths(self.year)[self.month-1]
        today = get_bs_today()

        row, col = 1, start_weekday
        for day in range(1, days_in_month + 1):
            is_weekend = col in (0, 6)
            is_today = (self.year == today["year"] and
                        self.month == today["month"] and
                        day == today["day"])

            bg = "#0066cc" if is_today else "#2a2a2a"
            fg = "white" if is_today else ("#ff5555" if is_weekend else "white")
            text = to_nepali_num(day) if USE_NEPALI else str(day)

            tk.Label(self.grid, text=text, width=4, height=2,
                     font=("Nirmala UI", 12, "bold"),
                     bg=bg, fg=fg, relief="flat").grid(
                row=row, column=col, padx=4, pady=3)

            col += 1
            if col > 6:
                col = 0
                row += 1

    def prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.draw_calendar()

    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.draw_calendar()

    def go_today(self):
        bs = get_bs_today()
        self.year = bs["year"]
        self.month = bs["month"]
        self.draw_calendar()

# ============================================================
# TRAY
# ============================================================
def create_icon():
    bs = get_bs_today()
    size = 48
    bg = (20, 140, 20, 255) if bs["weekday"] in (0, 6) else (220, 30, 30, 255)
    img = Image.new("RGBA", (size, size), bg)
    draw = ImageDraw.Draw(img)

    font = None
    for path in [r"C:\Windows\Fonts\mangalb.ttf", r"C:\Windows\Fonts\Nirmala.ttf"]:
        try:
            font = ImageFont.truetype(path, 40)
            break
        except:
            continue
    if font is None:
        font = ImageFont.load_default()

    text = to_nepali_num(bs["day"]) if USE_NEPALI else str(bs["day"])
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text(((size-tw)//2, (size-th)//2 - 22), text, fill=(255,255,255), font=font)
    return img

def get_tooltip():
    bs = get_bs_today()
    if USE_NEPALI:
        return f"{bs['month_name_np']} {to_nepali_num(bs['day'])}  {bs['weekday_np']}"
    return f"{bs['month_name_en']} {bs['day']}  {bs['weekday_en']}"

def open_calendar(icon=None, item=None):
    threading.Thread(target=NepaliCalendarWindow, daemon=True).start()

def toggle_overlay(icon, item):
    global SHOW_OVERLAY
    if SHOW_OVERLAY:
        close_overlay()
    else:
        SHOW_OVERLAY = True
        threading.Thread(target=run_overlay, daemon=True).start()
    update_menu(icon)

def toggle_always_on_top(icon, item):
    global ALWAYS_ON_TOP
    ALWAYS_ON_TOP = not ALWAYS_ON_TOP
    if overlay_root:
        try:
            overlay_root.attributes("-topmost", ALWAYS_ON_TOP)
        except:
            pass
    update_menu(icon)

def toggle_draggable(icon, item):
    global DRAGGABLE, SHOW_OVERLAY
    DRAGGABLE = not DRAGGABLE
    if SHOW_OVERLAY:
        close_overlay()
        time.sleep(0.12)
        SHOW_OVERLAY = True
        threading.Thread(target=run_overlay, daemon=True).start()
    update_menu(icon)

def toggle_language(icon, item):
    global USE_NEPALI
    USE_NEPALI = not USE_NEPALI
    icon.icon = create_icon()
    icon.title = get_tooltip()
    update_menu(icon)

def update_menu(icon):
    bs = get_bs_today()
    full = get_tooltip()

    if USE_NEPALI:
        menu = pystray.Menu(
            item("पात्रो खोल्नुहोस्", open_calendar, default=True),
            item(f"आज: {full}", None, enabled=False),
            item("ओभरले लुकाउनुहोस्" if SHOW_OVERLAY else "ओभरले देखाउनुहोस्", toggle_overlay),
            item("सधैं माथि" + (" ✓" if ALWAYS_ON_TOP else ""), toggle_always_on_top),
            item("तान्न मिल्ने" + (" ✓" if DRAGGABLE else ""), toggle_draggable),
            item("English", toggle_language),
            item("बन्द गर्नुहोस्", on_quit)
        )
    else:
        menu = pystray.Menu(
            item("Open Calendar", open_calendar, default=True),
            item(f"Today: {full}", None, enabled=False),
            item("Hide Overlay" if SHOW_OVERLAY else "Show Overlay", toggle_overlay),
            item("Always on Top" + (" ✓" if ALWAYS_ON_TOP else ""), toggle_always_on_top),
            item("Draggable" + (" ✓" if DRAGGABLE else ""), toggle_draggable),
            item("नेपाली", toggle_language),
            item("Quit", on_quit)
        )
    icon.menu = menu

def update_icon(icon):
    while True:
        icon.icon = create_icon()
        icon.title = get_tooltip()
        time.sleep(60)

def on_quit(icon, item):
    close_overlay()
    icon.stop()
    if lock_socket:
        lock_socket.close()

def main():
    icon = pystray.Icon("NepaliDate", create_icon(), get_tooltip())
    update_menu(icon)
    threading.Thread(target=update_icon, args=(icon,), daemon=True).start()
    icon.run()

if __name__ == "__main__":
    main()
