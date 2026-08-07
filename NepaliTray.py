import threading
import time
import socket
import sys
from PIL import Image, ImageDraw, ImageFont
import pystray
from pystray import MenuItem as item
import nepali_datetime
import tkinter as tk

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

# Settings
USE_NEPALI = True
SHOW_FULL_DATE = False          # False = day only, True = full short date


def to_nepali_num(num: int) -> str:
    digits = "०१२३४५६७८९"
    return "".join(digits[int(d)] for d in str(num))


class NepaliCalendarWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Nepali Calendar" if USE_NEPALI else "Calendar")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        win_w = 420
        win_h = 420

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        x = screen_w - win_w - 18
        y = screen_h - win_h - 50
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")

        self.current = nepali_datetime.date.today()
        self.year = self.current.year
        self.month = self.current.month

        self.setup_ui()
        self.draw_calendar()

        self.root.bind("<FocusOut>", self.on_focus_out)
        self.root.focus_force()
        self.root.mainloop()

    def on_focus_out(self, event):
        if event.widget == self.root:
            self.root.destroy()

    def setup_ui(self):
        outer = tk.Frame(self.root, bg="#1e1e1e")
        outer.pack(fill="both", expand=True, padx=16, pady=14)

        header = tk.Frame(outer, bg="#1e1e1e")
        header.pack(fill="x", pady=(2, 8))

        self.btn_prev = tk.Button(header, text="◀", font=("Segoe UI", 12, "bold"),
                                  bg="#333", fg="white", relief="flat", width=3,
                                  command=self.prev_month, cursor="hand2",
                                  activebackground="#555", activeforeground="white")
        self.btn_prev.pack(side="left", padx=4)

        self.lbl_title = tk.Label(header, text="", font=("Nirmala UI", 14, "bold"),
                                  bg="#1e1e1e", fg="white")
        self.lbl_title.pack(side="left", expand=True)

        self.btn_next = tk.Button(header, text="▶", font=("Segoe UI", 12, "bold"),
                                  bg="#333", fg="white", relief="flat", width=3,
                                  command=self.next_month, cursor="hand2",
                                  activebackground="#555", activeforeground="white")
        self.btn_next.pack(side="right", padx=4)

        self.calendar_frame = tk.Frame(outer, bg="#1e1e1e")
        self.calendar_frame.pack()

        if USE_NEPALI:
            weekdays = ["आइत", "सोम", "मंगल", "बुध", "बिहि", "शुक्र", "शनि"]
        else:
            weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        for i, day in enumerate(weekdays):
            color = "#ff5555" if i in (0, 6) else "#bbbbbb"
            lbl = tk.Label(self.calendar_frame, text=day, width=4,
                           font=("Nirmala UI", 10, "bold"),
                           bg="#1e1e1e", fg=color)
            lbl.grid(row=0, column=i, padx=4, pady=5)

        today_text = "आज" if USE_NEPALI else "Today"
        btn_today = tk.Button(outer, text=today_text, font=("Nirmala UI", 10),
                              bg="#444", fg="white", relief="flat",
                              command=self.go_today, cursor="hand2",
                              activebackground="#666", activeforeground="white")
        btn_today.pack(pady=(16, 4))

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
            is_weekend = (col == 0 or col == 6)
            is_today = (self.year == today.year and
                        self.month == today.month and
                        day == today.day)

            bg = "#2a2a2a"
            fg = "#ff5555" if is_weekend else "white"

            if is_today:
                bg = "#0066cc"
                fg = "white"

            day_text = to_nepali_num(day) if USE_NEPALI else str(day)

            lbl = tk.Label(self.calendar_frame, text=day_text, width=4, height=2,
                           font=("Nirmala UI", 12, "bold"),
                           bg=bg, fg=fg, relief="flat")
            lbl.grid(row=row, column=col, padx=4, pady=3)

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


def get_nepali_info():
    nd = nepali_datetime.date.today()
    day_np = nd.strftime("%D")
    day_en = str(nd.day)

    if USE_NEPALI:
        full = nd.strftime("%K %N %D  %G")
        short_full = nd.strftime("%N %D")          # e.g. श्रावण २२
    else:
        full = nd.strftime("%Y %B %d  %A")
        short_full = nd.strftime("%b %d")          # e.g. Shrawan 22

    is_weekend = nd.weekday() in (0, 6)
    return day_np, day_en, full, short_full, is_weekend


def create_icon(day_np, day_en, short_full, is_weekend):
    if SHOW_FULL_DATE:
        # Try wider icon for full date
        size = (120, 48)
        text = short_full
        font_size = 22
    else:
        size = (56, 56)
        text = day_np if USE_NEPALI else day_en
        font_size = 46

    bg = (20, 140, 20, 255) if is_weekend else (220, 30, 30, 255)
    image = Image.new("RGBA", size, bg)
    draw = ImageDraw.Draw(image)

    font = None
    for path in [r"C:\Windows\Fonts\mangalb.ttf"]:
        try:
            font = ImageFont.truetype(path, font_size)
            break
        except:
            continue
    if font is None:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    x = (size[0] - tw) // 2
    y = (size[1] - th) // 2 - (26 if not SHOW_FULL_DATE else 2)

    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    return image


def open_calendar(icon=None, item=None):
    threading.Thread(target=NepaliCalendarWindow, daemon=True).start()


def update_menu(icon):
    day_np, day_en, full, short_full, is_weekend = get_nepali_info()

    if USE_NEPALI:
        menu = pystray.Menu(
            item("पात्रो खोल्नुहोस्", open_calendar, default=True),
            item(f"आज: {full}", None, enabled=False),
            item("पूर्ण मिति देखाउनुहोस्" if not SHOW_FULL_DATE else "दिन मात्र देखाउनुहोस्", toggle_full_date),
            item("English", toggle_language),
            item("बन्द गर्नुहोस्", on_quit)
        )
    else:
        menu = pystray.Menu(
            item("Open Calendar", open_calendar, default=True),
            item(f"Today: {full}", None, enabled=False),
            item("Show Full Date" if not SHOW_FULL_DATE else "Show Day Only", toggle_full_date),
            item("नेपाली", toggle_language),
            item("Quit", on_quit)
        )

    icon.menu = menu


def toggle_language(icon, item):
    global USE_NEPALI
    USE_NEPALI = not USE_NEPALI

    day_np, day_en, full, short_full, is_weekend = get_nepali_info()
    icon.icon = create_icon(day_np, day_en, short_full, is_weekend)
    icon.title = full
    update_menu(icon)


def toggle_full_date(icon, item):
    global SHOW_FULL_DATE
    SHOW_FULL_DATE = not SHOW_FULL_DATE

    day_np, day_en, full, short_full, is_weekend = get_nepali_info()
    icon.icon = create_icon(day_np, day_en, short_full, is_weekend)
    icon.title = full
    update_menu(icon)


def update_icon(icon):
    while True:
        day_np, day_en, full, short_full, is_weekend = get_nepali_info()
        icon.icon = create_icon(day_np, day_en, short_full, is_weekend)
        icon.title = full
        time.sleep(60)


def on_quit(icon, item):
    icon.stop()
    if lock_socket:
        lock_socket.close()


def main():
    day_np, day_en, full, short_full, is_weekend = get_nepali_info()

    icon = pystray.Icon(
        name="NepaliDate",
        icon=create_icon(day_np, day_en, short_full, is_weekend),
        title=full
    )

    update_menu(icon)

    threading.Thread(target=update_icon, args=(icon,), daemon=True).start()
    icon.run()


if __name__ == "__main__":
    main()