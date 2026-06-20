import tkinter as tk
from tkinter import ttk, font as tkfont
from datetime import datetime, timedelta
import calendar
import random
import os
import json

# =========================
# THEME
# =========================
CRIMSON      = "#7A1B2E"
CRIMSON_DARK = "#5C1222"
CRIMSON_LITE = "#9B2438"
GOLD         = "#B8922A"
GOLD_LITE    = "#D4A843"
GOLD_FAINT   = "#FBF5E6"
PARCHMENT    = "#FAF7F2"
BORDER       = "#E8E0D0"
WHITE        = "#FFFFFF"
TEXT_DARK    = "#1A1410"
TEXT_MID     = "#5C5245"
TEXT_LIGHT   = "#9A8E82"
BANNER_TEXT  = "#FFF8F0"
BANNER_DIM   = "#D4C4B8"

# =========================
# DATA
# =========================
TODAY        = datetime.now().strftime("%Y-%m-%d")
TODAY_DISP   = datetime.now().strftime("%A, %B %d, %Y")
TODAY_MMDD   = datetime.now().strftime("%m-%d")
MONTH_KEY    = datetime.now().strftime("%Y-%m")

SAVE_DIR  = "save"
SAVE_FILE = os.path.join(SAVE_DIR, "daily_log.json")
SETT_FILE = os.path.join(SAVE_DIR, "settings.json")
os.makedirs(SAVE_DIR, exist_ok=True)

def load_json(path):
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

data     = load_json(SAVE_FILE)
settings = load_json(SETT_FILE)

# defaults
if "streaks"         not in settings: settings["streaks"]         = {"mass":0,"rosary":0,"reading":0}
if "last_streak_date" not in settings: settings["last_streak_date"] = TODAY
if "last_conf_date"  not in settings: settings["last_conf_date"]  = None
if "confessions"     not in settings: settings["confessions"]     = []
if "saints"          not in settings: settings["saints"]          = {}

SAINTS = [
    {"name": "St. Joseph",            "virtues": ["Obedience",   "Silence",      "Faithfulness"]},
    {"name": "St. Francis de Sales",  "virtues": ["Gentleness",  "Patience",     "Charity"]},
    {"name": "St. Thérèse of Lisieux","virtues": ["Humility",    "Trust",        "Love"]},
    {"name": "St. Teresa of Calcutta","virtues": ["Compassion",  "Service",      "Perseverance"]},
    {"name": "St. Augustine",         "virtues": ["Conversion",  "Intellect",    "Zeal"]},
    {"name": "St. Dominic",           "virtues": ["Penance",     "Prayer",       "Preaching"]},
]

if MONTH_KEY not in settings["saints"]:
    settings["saints"][MONTH_KEY] = random.choice(SAINTS)
SAINT = settings["saints"][MONTH_KEY]

FEASTS = {
    "01-01": "Solemnity of Mary",
    "01-28": "Saint Thomas Aquinas",
    "03-19": "St. Joseph",
    "03-25": "Annunciation",
    "06-13": "Saint Anthony of Padua",
    "06-19": "Sacred Heart of Jesus",
    "06-23": "Corpus Christi",
    "07-03": "Saint Thomas the Apostle",
    "07-16": "Our Lady of Mount Carmel",
    "08-15": "Assumption",
    "10-02": "Guardian Angels",
    "10-05": "Saint Faustina",
    "11-01": "All Saints",
    "12-08": "Immaculate Conception",
    "12-25": "Nativity of the Lord",
}

TASKS = [
    "Go to Mass with deepest devotion",
    "Reflect upon your main failing",
    "Spiritual reading",
    "Pray the Rosary",
    "Visit the Blessed Sacrament",
    "Meditate on the Passion of Christ",
    "Evening prayer and examination of conscience",
    "Begin and end activities with a Hail Mary",
]

STREAK_MAP = {
    "Go to Mass with deepest devotion": "mass",
    "Pray the Rosary":                  "rosary",
    "Spiritual reading":                "reading",
}

def season(month):
    if month in (11, 12): return "Advent"
    if month in (3, 4):   return "Lent / Easter"
    return "Ordinary Time"

# =========================
# STREAK UPDATE
# =========================
def update_streaks():
    last = settings.get("last_streak_date")
    if last == TODAY:
        return
    prev = data.get(last, {})
    for task, cat in STREAK_MAP.items():
        if prev.get(task):
            settings["streaks"][cat] = settings["streaks"].get(cat, 0) + 1
        else:
            settings["streaks"][cat] = 0
    settings["last_streak_date"] = TODAY

# daily reset
if settings.get("last_open_date") != TODAY:
    if TODAY not in data:
        data[TODAY] = {}
    update_streaks()
    settings["last_open_date"] = TODAY

# =========================
# SAVE
# =========================
checkbox_vars = {}

def save_all():
    data[TODAY] = {t: v.get() for t, v in checkbox_vars.items()}
    with open(SAVE_FILE, "w") as f: json.dump(data, f, indent=2)
    with open(SETT_FILE, "w") as f: json.dump(settings, f, indent=2)

# =========================
# ROOT & FONTS
# =========================
root = tk.Tk()
root.title("Seelos — Rule of Life")
root.geometry("780x920")
root.configure(bg=PARCHMENT)
root.resizable(True, True)

try:
    serif = tkfont.Font(family="Georgia", size=11)
    serif_lg = tkfont.Font(family="Georgia", size=18, weight="bold")
    serif_md = tkfont.Font(family="Georgia", size=13)
    sans = tkfont.Font(family="Helvetica Neue", size=11)
    sans_sm = tkfont.Font(family="Helvetica Neue", size=10)
    sans_lg = tkfont.Font(family="Helvetica Neue", size=13)
    sans_bold = tkfont.Font(family="Helvetica Neue", size=11, weight="bold")
    mono_lg = tkfont.Font(family="Courier", size=28, weight="bold")
except Exception:
    serif = ("Times", 11)
    serif_lg = ("Times", 18, "bold")
    serif_md = ("Times", 13)
    sans = ("Helvetica", 11)
    sans_sm = ("Helvetica", 10)
    sans_lg = ("Helvetica", 13)
    sans_bold = ("Helvetica", 11, "bold")
    mono_lg = ("Courier", 28, "bold")

# =========================
# SCROLLABLE SHELL
# =========================
outer = tk.Frame(root, bg=PARCHMENT)
outer.pack(fill="both", expand=True)

canvas = tk.Canvas(outer, bg=PARCHMENT, highlightthickness=0)
scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

main = tk.Frame(canvas, bg=PARCHMENT)
win_id = canvas.create_window((0, 0), window=main, anchor="nw")

def on_configure(e):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_canvas_resize(e):
    canvas.itemconfig(win_id, width=e.width)

main.bind("<Configure>", on_configure)
canvas.bind("<Configure>", on_canvas_resize)

def _scroll(event):
    if event.delta:
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    elif event.num == 4:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        canvas.yview_scroll(1, "units")

canvas.bind_all("<MouseWheel>", _scroll)
canvas.bind_all("<Button-4>", _scroll)
canvas.bind_all("<Button-5>", _scroll)

# =========================
# HELPERS
# =========================
def card(parent, pady=(0, 8)):
    f = tk.Frame(parent, bg=WHITE, bd=0, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER)
    f.pack(fill="x", padx=16, pady=pady)
    return f

def section_label(parent, text):
    tk.Label(parent, text=text.upper(), font=sans_sm, bg=WHITE,
             fg=CRIMSON).pack(anchor="w", padx=16, pady=(14, 4))

def divider(parent):
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=16)

# =========================
# BANNER
# =========================
banner = tk.Frame(main, bg=CRIMSON)
banner.pack(fill="x")

tk.Label(banner, text="✠ Blessed Francis Xavier Seelos ✠",
         font=serif_lg, bg=CRIMSON, fg=BANNER_TEXT).pack(pady=(20, 4))

tk.Label(banner, text="A Practical Guide to Holiness",
         font=serif_md, bg=CRIMSON, fg=GOLD_LITE).pack(pady=(2, 0))

tk.Label(banner, text=TODAY_DISP,
         font=sans_sm, bg=CRIMSON, fg=BANNER_DIM).pack()

meta_row = tk.Frame(banner, bg=CRIMSON)
meta_row.pack(pady=(8, 20))

tk.Label(meta_row, text=f"  {season(datetime.now().month)}  ",
         font=sans_sm, bg=CRIMSON_DARK, fg=BANNER_DIM,
         padx=8, pady=3, relief="flat").pack(side="left", padx=4)

feast = FEASTS.get(TODAY_MMDD)
if feast:
    tk.Label(meta_row, text=f"  {feast}  ",
             font=sans_sm, bg="#6B2800", fg="#FFD97A",
             padx=8, pady=3).pack(side="left", padx=4)

# =========================
# NAV TABS
# =========================
tab_bar = tk.Frame(main, bg=WHITE, highlightthickness=1, highlightbackground=BORDER)
tab_bar.pack(fill="x")

content_frames = {}
active_tab = tk.StringVar(value="today")

def switch_tab(name, btn):
    for k, f in content_frames.items():
        f.pack_forget()
    content_frames[name].pack(fill="x")
    for b in tab_buttons:
        b.configure(fg=TEXT_MID, relief="flat", bd=0,
                    bg=WHITE, font=sans)
    btn.configure(fg=CRIMSON, font=sans_bold,
                  relief="flat", bd=0, bg=WHITE)
    active_tab.set(name)
    if name == "calendar":
        render_calendar()

tab_buttons = []
for tab_id, label in [("today","Today"), ("calendar","Calendar"), ("confession","Confession")]:
    b = tk.Button(tab_bar, text=label, font=sans,
                  bg=WHITE, fg=TEXT_MID, bd=0, relief="flat",
                  pady=10, cursor="hand2",
                  activebackground=GOLD_FAINT, activeforeground=CRIMSON)
    b.pack(side="left", fill="x", expand=True)
    b.configure(command=lambda n=tab_id, btn=b: switch_tab(n, btn))
    tab_buttons.append(b)

# Activate today tab visually
tab_buttons[0].configure(fg=CRIMSON, font=sans_bold)

# =========================
# TODAY TAB
# =========================
today_frame = tk.Frame(main, bg=PARCHMENT)
content_frames["today"] = today_frame

# --- Saint ---
c = card(today_frame, pady=(12, 0))
section_label(c, "Saint of the Month")
divider(c)
saint_inner = tk.Frame(c, bg=WHITE)
saint_inner.pack(fill="x", padx=16, pady=10)
tk.Label(saint_inner, text=SAINT["name"], font=serif_md,
         bg=WHITE, fg=CRIMSON).pack(anchor="w")
virtues_row = tk.Frame(saint_inner, bg=WHITE)
virtues_row.pack(anchor="w", pady=(4, 0))
for v in SAINT["virtues"]:
    tk.Label(virtues_row, text=f"  {v}  ", font=sans_sm,
             bg=GOLD_FAINT, fg="#7A6010", relief="flat",
             padx=4, pady=2).pack(side="left", padx=3)

# --- Progress ---
c2 = card(today_frame, pady=(8, 0))
section_label(c2, "Daily Progress")
divider(c2)
prog_inner = tk.Frame(c2, bg=WHITE)
prog_inner.pack(fill="x", padx=16, pady=10)

progress_label = tk.Label(prog_inner, text="0 of 8 complete",
                           font=sans_sm, bg=WHITE, fg=TEXT_MID)
progress_label.pack(anchor="w", pady=(0, 6))

prog_canvas = tk.Canvas(prog_inner, bg=BORDER, height=7, bd=0,
                         highlightthickness=0)
prog_canvas.pack(fill="x")
prog_bar_rect = prog_canvas.create_rectangle(0, 0, 0, 7, fill=GOLD, outline="")

def update_progress_bar():
    prog_canvas.update_idletasks()
    w = prog_canvas.winfo_width()
    done = sum(v.get() for v in checkbox_vars.values())
    pct = done / len(TASKS)
    prog_canvas.coords(prog_bar_rect, 0, 0, int(w * pct), 7)
    progress_label.config(text=f"{done} of {len(TASKS)} complete")

# Streaks row
streak_row = tk.Frame(c2, bg=WHITE)
streak_row.pack(fill="x", padx=16, pady=(0, 12))

streak_labels = {}
for cat, label in [("mass","Mass streak"), ("rosary","Rosary streak"), ("reading","Reading streak")]:
    box = tk.Frame(streak_row, bg=PARCHMENT, relief="flat",
                   highlightthickness=1, highlightbackground=BORDER)
    box.pack(side="left", expand=True, fill="x", padx=4, pady=4)
    num = tk.Label(box, text=str(settings["streaks"].get(cat, 0)),
                   font=("Helvetica", 22, "bold"), bg=PARCHMENT, fg=CRIMSON)
    num.pack(pady=(8, 2))
    tk.Label(box, text=label, font=sans_sm, bg=PARCHMENT,
             fg=TEXT_MID).pack(pady=(0, 8))
    streak_labels[cat] = num

def refresh_streaks():
    for cat, lbl in streak_labels.items():
        lbl.config(text=str(settings["streaks"].get(cat, 0)))

# --- Checklist ---
c3 = card(today_frame, pady=(8, 16))
section_label(c3, "Rule of Life")
divider(c3)

task_inner = tk.Frame(c3, bg=WHITE)
task_inner.pack(fill="x", padx=12, pady=8)

for t in TASKS:
    v = tk.BooleanVar()
    checkbox_vars[t] = v
    row = tk.Frame(task_inner, bg=WHITE)
    row.pack(fill="x", pady=2)
    cb = tk.Checkbutton(
        row, text=f"  {t}", variable=v,
        font=sans, bg=WHITE, fg=TEXT_DARK,
        selectcolor=GOLD_FAINT, activebackground=WHITE,
        activeforeground=CRIMSON,
        indicatoron=True,
        command=lambda: (update_progress_bar(), save_all())
    )
    cb.pack(anchor="w", padx=4)

# restore state
if TODAY in data:
    for t, v in checkbox_vars.items():
        if t in data[TODAY]:
            v.set(data[TODAY][t])

# =========================
# CALENDAR TAB
# =========================
cal_frame = tk.Frame(main, bg=PARCHMENT)
content_frames["calendar"] = cal_frame

cal_state = {"year": datetime.now().year, "month": datetime.now().month}
cal_detail_frame = None

def render_calendar():
    global cal_detail_frame
    for widget in cal_frame.winfo_children():
        widget.destroy()
    cal_detail_frame = None

    c = card(cal_frame, pady=(12, 16))

    # header
    hdr = tk.Frame(c, bg=WHITE)
    hdr.pack(fill="x", padx=16, pady=(10, 6))

    year  = cal_state["year"]
    month = cal_state["month"]
    month_name = datetime(year, month, 1).strftime("%B %Y")

    tk.Label(hdr, text=month_name, font=sans_bold,
             bg=WHITE, fg=TEXT_DARK).pack(side="left")

    nav = tk.Frame(hdr, bg=WHITE)
    nav.pack(side="right")

    def go_prev():
        if cal_state["month"] == 1:
            cal_state["month"] = 12; cal_state["year"] -= 1
        else:
            cal_state["month"] -= 1
        render_calendar()

    def go_next():
        if cal_state["month"] == 12:
            cal_state["month"] = 1; cal_state["year"] += 1
        else:
            cal_state["month"] += 1
        render_calendar()

    tk.Button(nav, text="‹", font=sans_lg, bg=WHITE, fg=CRIMSON,
              bd=0, relief="flat", cursor="hand2",
              command=go_prev).pack(side="left", padx=6)
    tk.Button(nav, text="›", font=sans_lg, bg=WHITE, fg=CRIMSON,
              bd=0, relief="flat", cursor="hand2",
              command=go_next).pack(side="left")

    divider(c)

    grid_frame = tk.Frame(c, bg=WHITE)
    grid_frame.pack(fill="x", padx=16, pady=8)

    for i, dow in enumerate(["Su","Mo","Tu","We","Th","Fr","Sa"]):
        tk.Label(grid_frame, text=dow, font=sans_sm, bg=WHITE,
                 fg=TEXT_LIGHT, width=5).grid(row=0, column=i, pady=(0, 4))

    first_day = datetime(year, month, 1)
    start_col = first_day.weekday() + 1  # Mon=0 → col 1; Sun col 0
    if start_col == 7: start_col = 0     # Sunday correction

    days_in_month = calendar.monthrange(year, month)[1]
    today_dt = datetime.strptime(TODAY, "%Y-%m-%d")

    selected_btn = [None]

    def day_click(d_str, btn):
        if selected_btn[0]:
            # reset old
            old_d = int(selected_btn[0].cget("text"))
            old_str = f"{year}-{month:02d}-{old_d:02d}"
            log_ = data.get(old_str, {})
            done_ = sum(1 for t in TASKS if log_.get(t))
            if old_str == TODAY:
                selected_btn[0].configure(
                    bg="#F0E8D8", fg=CRIMSON,
                    relief="flat", highlightbackground=CRIMSON)
            else:
                col_ = WHITE if done_ == 0 else (GOLD_FAINT if done_ == len(TASKS) else PARCHMENT)
                selected_btn[0].configure(bg=col_, relief="flat")
        selected_btn[0] = btn
        btn.configure(bg=CRIMSON, fg=BANNER_TEXT, relief="flat")
        show_day_detail(d_str, c)

    for day in range(1, days_in_month + 1):
        col = (start_col + day - 1) % 7
        row = (start_col + day - 1) // 7 + 1
        d_str = f"{year}-{month:02d}-{day:02d}"
        log = data.get(d_str, {})
        done = sum(1 for t in TASKS if log.get(t))

        is_today = (d_str == TODAY)
        is_future = datetime(year, month, day) > today_dt

        if is_today:
            bg = "#F0E8D8"; fg = CRIMSON
        elif is_future:
            bg = WHITE; fg = TEXT_LIGHT
        elif done == len(TASKS):
            bg = GOLD_FAINT; fg = TEXT_DARK
        elif done > 0:
            bg = PARCHMENT; fg = TEXT_DARK
        else:
            bg = WHITE; fg = TEXT_LIGHT

        btn = tk.Button(
            grid_frame, text=str(day), font=sans_sm,
            bg=bg, fg=fg, width=4, height=2,
            bd=0, relief="flat", cursor="hand2",
            highlightthickness=(1 if is_today else 0),
            highlightbackground=CRIMSON
        )
        btn.grid(row=row, column=col, padx=2, pady=2)
        if not is_future:
            btn.configure(command=lambda ds=d_str, b=btn: day_click(ds, b))

    # legend
    leg = tk.Frame(c, bg=WHITE)
    leg.pack(anchor="w", padx=16, pady=(4, 12))
    for color, label in [(GOLD_FAINT,"All complete"),(PARCHMENT,"Partial"),(WHITE,"None")]:
        dot = tk.Frame(leg, bg=color, width=14, height=14,
                       highlightthickness=1, highlightbackground=BORDER)
        dot.pack(side="left")
        tk.Label(leg, text=label, font=sans_sm, bg=WHITE,
                 fg=TEXT_MID).pack(side="left", padx=(3, 10))


def show_day_detail(d_str, parent):
    global cal_detail_frame
    if cal_detail_frame:
        cal_detail_frame.destroy()

    cal_detail_frame = tk.Frame(parent, bg=PARCHMENT,
                                 highlightthickness=1,
                                 highlightbackground=BORDER)
    cal_detail_frame.pack(fill="x", padx=16, pady=(0, 12))

    dt = datetime.strptime(d_str, "%Y-%m-%d")
    label = dt.strftime("%A, %B %d, %Y")
    log = data.get(d_str, {})
    done = sum(1 for t in TASKS if log.get(t))
    pct = int(done / len(TASKS) * 100)

    tk.Label(cal_detail_frame,
             text=f"{label}  —  {pct}% complete",
             font=sans_bold, bg=PARCHMENT, fg=CRIMSON).pack(anchor="w", padx=12, pady=(10, 6))

    for t in TASKS:
        ok = bool(log.get(t))
        row = tk.Frame(cal_detail_frame, bg=PARCHMENT)
        row.pack(fill="x", padx=12, pady=1)
        mark = "✓" if ok else "–"
        fg   = GOLD if ok else TEXT_LIGHT
        tk.Label(row, text=mark, font=sans_bold, bg=PARCHMENT,
                 fg=fg, width=2).pack(side="left")
        tk.Label(row, text=t, font=sans_sm, bg=PARCHMENT,
                 fg=TEXT_DARK if ok else TEXT_LIGHT).pack(side="left")

    tk.Frame(cal_detail_frame, bg=PARCHMENT, height=10).pack()

# =========================
# CONFESSION TAB
# =========================
conf_frame = tk.Frame(main, bg=PARCHMENT)
content_frames["confession"] = conf_frame

def get_conf_days():
    last = settings.get("last_conf_date")
    if not last:
        return None
    last_dt = datetime.strptime(last, "%Y-%m-%d")
    today_dt = datetime.strptime(TODAY, "%Y-%m-%d")
    return (today_dt - last_dt).days

conf_days_lbl = None
conf_date_lbl = None
conf_hist_frame = None

def build_confession_tab():
    global conf_days_lbl, conf_date_lbl, conf_hist_frame

    for w in conf_frame.winfo_children():
        w.destroy()

    c = card(conf_frame, pady=(12, 0))
    section_label(c, "Last Confession")
    divider(c)

    inner = tk.Frame(c, bg=WHITE)
    inner.pack(fill="x", padx=16, pady=12)

    days = get_conf_days()
    day_str = str(days) if days is not None else "—"
    sub_str = ("day" if days == 1 else "days") + " since last confession" if days is not None else "No confession recorded yet"

    conf_days_lbl = tk.Label(inner, text=day_str,
                              font=("Helvetica", 36, "bold"),
                              bg=WHITE, fg=CRIMSON)
    conf_days_lbl.pack(anchor="w")

    conf_date_lbl = tk.Label(inner, text=sub_str, font=sans, bg=WHITE, fg=TEXT_MID)
    conf_date_lbl.pack(anchor="w", pady=(2, 0))

    last = settings.get("last_conf_date")
    if last:
        dt = datetime.strptime(last, "%Y-%m-%d")
        tk.Label(inner, text="Last: " + dt.strftime("%A, %B %d, %Y"),
                 font=sans_sm, bg=WHITE, fg=TEXT_LIGHT).pack(anchor="w", pady=(4, 0))

    def log_conf():
        settings["last_conf_date"] = TODAY
        if not settings.get("confessions"):
            settings["confessions"] = []
        if not settings["confessions"] or settings["confessions"][0] != TODAY:
            settings["confessions"].insert(0, TODAY)
        save_all()
        build_confession_tab()

    btn = tk.Label(inner, text="✓  I went to confession today",
                   font=("Georgia", 13, "bold"), bg=CRIMSON_DARK, fg="#FFFFFF",
                   cursor="hand2", pady=12, padx=20, relief="flat")
    btn.pack(fill="x", pady=(14, 4))
    btn.bind("<Button-1>", lambda e: log_conf())
    btn.bind("<Enter>",    lambda e: btn.configure(bg="#3D0C18"))
    btn.bind("<Leave>",    lambda e: btn.configure(bg=CRIMSON_DARK))

    # History
    c2 = card(conf_frame, pady=(8, 16))
    section_label(c2, "Confession History")
    divider(c2)

    hist_inner = tk.Frame(c2, bg=WHITE)
    hist_inner.pack(fill="x", padx=16, pady=8)

    confessions = settings.get("confessions", [])
    if not confessions:
        tk.Label(hist_inner, text="No history recorded yet.",
                 font=sans_sm, bg=WHITE, fg=TEXT_LIGHT).pack(anchor="w")
    else:
        for i, d in enumerate(confessions[:15]):
            dt = datetime.strptime(d, "%Y-%m-%d")
            row = tk.Frame(hist_inner, bg=WHITE)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=dt.strftime("%A, %B %d, %Y"),
                     font=sans, bg=WHITE, fg=TEXT_DARK).pack(side="left")
            if i + 1 < len(confessions):
                prev = datetime.strptime(confessions[i + 1], "%Y-%m-%d")
                gap = (dt - prev).days
                tk.Label(row, text=f"{gap}d gap",
                         font=sans_sm, bg=WHITE, fg=TEXT_LIGHT).pack(side="right")
            tk.Frame(hist_inner, bg=BORDER, height=1).pack(fill="x", pady=(3, 0))

build_confession_tab()

# show today by default
content_frames["today"].pack(fill="x")

# =========================
# SAVE BUTTON
# =========================
save_btn = tk.Button(
    main, text="  ✦  Save  ✦  ", font=sans_bold,
    bg=GOLD_FAINT, fg=CRIMSON, bd=0, relief="flat",
    padx=24, pady=10, cursor="hand2",
    highlightthickness=1, highlightbackground=GOLD,
    activebackground=GOLD_FAINT, activeforeground=CRIMSON_DARK,
    command=save_all
)
save_btn.pack(pady=(8, 24))

# =========================
# INIT
# =========================
root.after(100, update_progress_bar)

def on_close():
    save_all()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()