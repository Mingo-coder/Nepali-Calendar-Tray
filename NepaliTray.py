import threading
import time
import socket
import sys
import ctypes
from ctypes import wintypes
from PIL import Image, ImageDraw, ImageFont
import pystray
from pystray import MenuItem as item
import nepali_datetime
import tkinter as tk
from tkinter import font as tkfont

# ========== Single Instance Lock ==========
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
# =========================================

# Global settings
USE_NEPALI = True
SHOW_OVERLAY = False
ALWAYS_ON_TOP = True
DRAGGABLE = True
CALENDAR_STAY_OPEN = False

LAST_OVERLAY_X = None
LAST_OVERLAY_Y = None
overlay_root = None

# Win32 constants for click-through
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020

user32 = ctypes.windll.user32


def set_click_through(hwnd, enable: bool):
    """Enable or disable click-through on a window"""
    try:
        style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        if enable:
            style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
        else:
            style &= ~WS_EX_TRANSPARENT
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    except Exception as e:
        print("Click-through error:", e)


def to_nepali_num(num: int) -> str:
    digits = "०१२३४५६७८९"
    return "".join(digits[int(d)] for d in str(num))


# ==================== OVERLAY ====================
class DateOverlay:
    def __init__(self):
        global overlay_root, LAST_OVERLAY_X, LAST_OVERLAY_Y
        self.root = tk.Tk()
        overlay_root = self.root

        self.root.title("NepaliDateOverlay")
        self.root.overrideredirect(True)
        self.root.configure(bg="#111111")
        self.root.attributes("-alpha", 0.88)

        try:
            self.font = tkfont.Font(family="Nirmala UI", size=13, weight="bold")
        except:
            self.font = tkfont.Font(family="Segoe UI", size=13, weight="bold")

        self.label = tk.Label(
            self.root, text="", font=self.font,
            fg="white", bg="#111111", padx=16, pady=8
        )
        self.label.pack()

        self.apply_always_on_top()
        self.apply_draggable_and_clickthrough()

        self.update_date()

        if LAST_OVERLAY_X is not None and LAST_OVERLAY_Y is not None:
            self.root.geometry(f"+{LAST_OVERLAY_X}+{LAST_OVERLAY_Y}")
        else:
            self.position_window()

        self.schedule_update()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def apply_always_on_top(self):
        self.root.attributes("-topmost", ALWAYS_ON_TOP)

    def apply_draggable_and_clickthrough(self):
        hwnd = self.root.winfo_id()

        # Clear bindings
        self.root.unbind("<Button-1>")
        self.root.unbind("<B1-Motion>")
        self.label.unbind("<Button-1>")
        self.label.unbind("<B1-Motion>")

        if DRAGGABLE:
            set_click_through(hwnd, False)
            self.root.bind("<Button-1>", self.start_move)
            self.root.bind("<B1-Motion>", self.do_move)
            self.label.bind("<Button-1>", self.start_move)
            self.label.bind("<B1-Motion>", self.do_move)
        else:
            # Enable real click-through
            set_click_through(hwnd, True)

    def update_date(self):
        nd = nepali_datetime.date.today()
        if USE_NEPALI:
            text = nd.strftime("%N %D, %G")
        else:
            text = nd.strftime("%B %d, %A")

        color = "#ff5555" if nd.weekday() in (0, 6) else "white"
        self.label.config(text=text, fg=color)

    def position_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = screen_w - width - 200
        y = screen_h - height - 48
        self.root.geometry(f"+{x}+{y}")

    def schedule_update(self):
        if self.root.winfo_exists():
            self.update_date()
            self.root.after(20000, self.schedule_update)

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def do_move(self, event):
        global LAST_OVERLAY_X, LAST_OVERLAY_Y
        x = self.root.winfo_x() + (event.x - self._x)
        y = self.root.winfo_y() + (event.y - self._y)
        self.root.geometry(f"+{x}+{y}")
        LAST_OVERLAY_X = x
        LAST_OVERLAY_Y = y

    def on_close(self):
        global SHOW_OVERLAY, overlay_root, LAST_OVERLAY_X, LAST_OVERLAY_Y
        try:
            LAST_OVERLAY_X = self.root.winfo_x()
            LAST_OVERLAY_Y = self.root.winfo_y()
        except:
            pass
        SHOW_OVERLAY = False
        overlay_root = None
        self.root.destroy()


def run_overlay():
    DateOverlay()


def close_overlay():
    global overlay_root, SHOW_OVERLAY, LAST_OVERLAY_X, LAST_OVERLAY_Y
    if overlay_root is not None:
        try:
            LAST_OVERLAY_X = overlay_root.winfo_x()
            LAST_OVERLAY_Y = overlay_root.winfo_y()
            overlay_root.after(0, overlay_root.destroy)
        except:
            pass
        overlay_root = None
    SHOW_OVERLAY = False


# ==================== CALENDAR ====================
class NepaliCalendarWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Nepali Calendar" if USE_NEPALI else "Calendar")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        win_w, win_h = 420, 420
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = screen_w - win_w - 18
        y = screen_h - win_h - 50
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")

        self.year = nepali_datetime.date.today().year
        self.month = nepali_datetime.date.today().month

        self.setup_ui()
        self.draw_calendar()

        self.root.bind("<FocusOut>", self.on_focus_out)
        self.root.focus_force()
        self.root.mainloop()

    def on_focus_out(self, event):
        if not CALENDAR_STAY_OPEN:
            try:
                self.root.destroy()
            except:
                pass

    def toggle_pin(self):
        global CALENDAR_STAY_OPEN
        CALENDAR_STAY_OPEN = not CALENDAR_STAY_OPEN
        self.update_pin_button()

    def update_pin_button(self):
        if CALENDAR_STAY_OPEN:
            self.btn_pin.config(text="📌", bg="#0066cc")  # pinned
        else:
            self.btn_pin.config(text="📍", bg="#333")     # unpinned

    def setup_ui(self):
        outer = tk.Frame(self.root, bg="#1e1e1e")
        outer.pack(fill="both", expand=True, padx=16, pady=14)

        # Header
        header = tk.Frame(outer, bg="#1e1e1e")
        header.pack(fill="x", pady=(2, 8))

        self.btn_prev = tk.Button(header, text="◀", font=("Segoe UI", 12, "bold"),
                                  bg="#333", fg="white", relief="flat", width=3,
                                  command=self.prev_month, cursor="hand2")
        self.btn_prev.pack(side="left", padx=4)

        # Month title
        self.lbl_title = tk.Label(header, text="", font=("Nirmala UI", 14, "bold"),
                                  bg="#1e1e1e", fg="white")
        self.lbl_title.pack(side="left", expand=True)

        # Pin button (next to the month)
        self.btn_pin = tk.Button(header, text="📍", font=("Segoe UI", 11),
                                 bg="#333", fg="white", relief="flat", width=3,
                                 command=self.toggle_pin, cursor="hand2")
        self.btn_pin.pack(side="left", padx=(6, 4))
        self.update_pin_button()

        self.btn_next = tk.Button(header, text="▶", font=("Segoe UI", 12, "bold"),
                                  bg="#333", fg="white", relief="flat", width=3,
                                  command=self.next_month, cursor="hand2")
        self.btn_next.pack(side="right", padx=4)

        self.calendar_frame = tk.Frame(outer, bg="#1e1e1e")
        self.calendar_frame.pack()

        weekdays = ["आइत", "सोम", "मंगल", "बुध", "बिहि", "शुक्र", "शनि"] if USE_NEPALI else \
                   ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        for i, day in enumerate(weekdays):
            color = "#ff5555" if i in (0, 6) else "#bbbbbb"
            lbl = tk.Label(self.calendar_frame, text=day, width=4,
                           font=("Nirmala UI", 10, "bold"),
                           bg="#1e1e1e", fg=color)
            lbl.grid(row=0, column=i, padx=4, pady=5)

        today_text = "आज" if USE_NEPALI else "Today"
        tk.Button(outer, text=today_text, font=("Nirmala UI", 10),
                  bg="#444", fg="white", relief="flat",
                  command=self.go_today, cursor="hand2").pack(pady=(16, 4))

    def draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        if USE_NEPALI:
            month_name = nepali_datetime.date(self.year, self.month, 1).strftime("%N %K")
        else:
            month_name = nepali_datetime.date(self.year, self.month, 1).strftime("%B %Y")

        self.lbl_title.config(text=month_name)

        first = nepali_datetime.date(self.year, self.month, 1)
        start_weekday = first.weekday()

        if self.month == 12:
            next_month = nepali_datetime.date(self.year + 1, 1, 1)
        else:
            next_month = nepali_datetime.date(self.year, self.month + 1, 1)
        days_in_month = (next_month - first).days

        today = nepali_datetime.date.today()
        row = 1
        col = start_weekday

        for day in range(1, days_in_month + 1):
            is_weekend = col in (0, 6)
            is_today = (self.year == today.year and self.month == today.month and day == today.day)

            bg = "#0066cc" if is_today else "#2a2a2a"
            fg = "white" if is_today else ("#ff5555" if is_weekend else "white")

            day_text = to_nepali_num(day) if USE_NEPALI else str(day)

            tk.Label(self.calendar_frame, text=day_text, width=4, height=2,
                     font=("Nirmala UI", 12, "bold"),
                     bg=bg, fg=fg, relief="flat").grid(row=row, column=col, padx=4, pady=3)

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
        today = nepali_datetime.date.today()
        self.year = today.year
        self.month = today.month
        self.draw_calendar()


# ==================== TRAY ====================
def get_nepali_info():
    nd = nepali_datetime.date.today()
    day_np = nd.strftime("%D")
    day_en = str(nd.day)
    full = nd.strftime("%K %N %D  %G") if USE_NEPALI else nd.strftime("%Y %B %d  %A")
    is_weekend = nd.weekday() in (0, 6)
    return day_np, day_en, full, is_weekend


def create_icon(day_np, day_en, is_weekend):
    size = 48
    bg = (220, 30, 30, 255) if is_weekend else (0, 0, 0, 0)
    image = Image.new("RGBA", (size, size), bg)
    draw = ImageDraw.Draw(image)

    font = None
    for path in [r"C:\Windows\Fonts\mangalb.ttf", r"C:\Windows\Fonts\Nirmala.ttf"]:
        try:
            font = ImageFont.truetype(path, 40)
            break
        except:
            continue
    if font is None:
        font = ImageFont.load_default()

    text = day_np if USE_NEPALI else day_en
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    x = (size - tw) // 2
    y = (size - th) // 2 - 22
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    return image


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
    if overlay_root is not None:
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
    day_np, day_en, full, is_weekend = get_nepali_info()
    icon.icon = create_icon(day_np, day_en, is_weekend)
    icon.title = full
    update_menu(icon)


def update_menu(icon):
    day_np, day_en, full, is_weekend = get_nepali_info()

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
        day_np, day_en, full, is_weekend = get_nepali_info()
        icon.icon = create_icon(day_np, day_en, is_weekend)
        icon.title = full
        time.sleep(60)


def on_quit(icon, item):
    close_overlay()
    icon.stop()
    if lock_socket:
        lock_socket.close()


def main():
    day_np, day_en, full, is_weekend = get_nepali_info()

    icon = pystray.Icon(
        name="NepaliDate",
        icon=create_icon(day_np, day_en, is_weekend),
        title=full
    )

    update_menu(icon)
    threading.Thread(target=update_icon, args=(icon,), daemon=True).start()
    icon.run()


if __name__ == "__main__":
    main()
