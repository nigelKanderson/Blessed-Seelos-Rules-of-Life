import tkinter as tk
from datetime import datetime
import random
import os
import json

# =========================
# DATE
# =========================
today_date = datetime.now().strftime("%Y-%m-%d")
today_display = datetime.now().strftime("%B %d, %Y")
current_month = datetime.now().strftime("%Y-%m")
today_mmdd = datetime.now().strftime("%m-%d")

# =========================
# COLORS (SIMPLE FIXED STYLE)
# =========================
BG = "#F5F1E8"
CARD = "#FFFFFF"
TEXT = "#2B2B2B"
ACCENT = "#6B1F2B"
GOLD = "#C8A24A"

# =========================
# FILES
# =========================
SAVE_DIR = "save"
SAVE_FILE = os.path.join(SAVE_DIR, "daily_log.json")
SETTINGS_FILE = os.path.join(SAVE_DIR, "settings.json")

os.makedirs(SAVE_DIR, exist_ok=True)

def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

data = load_json(SAVE_FILE)
settings = load_json(SETTINGS_FILE)

# =========================
# DAILY RESET
# =========================
last_open_date = settings.get("last_open_date")

if last_open_date != today_date:
    data[today_date] = {}
    settings["last_open_date"] = today_date

# =========================
# STREAKS
# =========================
if "streaks" not in settings:
    settings["streaks"] = {"mass": 0, "rosary": 0, "reading": 0}

if "last_streak_date" not in settings:
    settings["last_streak_date"] = today_date

streak_map = {
    "Go to Mass with deepest devotion": "mass",
    "Pray the Rosary": "rosary",
    "Spiritual reading": "reading"
}

def update_streaks():
    last = settings.get("last_streak_date")
    if last == today_date:
        return

    previous = data.get(last, {})

    for task, cat in streak_map.items():
        if previous.get(task, False):
            settings["streaks"][cat] += 1
        else:
            settings["streaks"][cat] = 0

    settings["last_streak_date"] = today_date

# =========================
# SAINTS
# =========================
saints = [
    {"name": "St. Joseph", "virtues": ["Obedience", "Silence", "Faithfulness"]},
    {"name": "St. Francis de Sales", "virtues": ["Gentleness", "Patience", "Charity"]},
    {"name": "St. Thérèse of Lisieux", "virtues": ["Humility", "Trust", "Love"]},
    {"name": "St. Teresa of Calcutta", "virtues": ["Compassion", "Service", "Perseverance"]}
]

if current_month in settings:
    saint = settings[current_month]
else:
    saint = random.choice(saints)
    settings[current_month] = saint

# =========================
# TASKS
# =========================
tasks = [
    "Go to Mass with deepest devotion",
    "Reflect upon your main failing",
    "Spiritual reading",
    "Pray the Rosary",
    "Visit the Blessed Sacrament",
    "Meditate on the Passion of Christ",
    "Evening prayer and examination of conscience",
    "Begin and end activities with a Hail Mary"
]

checkbox_vars = {}

# =========================
# CALENDAR
# =========================
feasts = {
    "01-01": "Solemnity of Mary",
    "03-19": "St. Joseph",
    "03-25": "Annunciation",
    "06-19": "Sacred Heart of Jesus",
    "08-15": "Assumption",
    "10-02": "Guardian Angels",
    "11-01": "All Saints",
    "12-08": "Immaculate Conception",
    "12-25": "Nativity of the Lord"
}

def season(month):
    if month in [11, 12]:
        return "Advent / Transition"
    elif month in [3, 4]:
        return "Lent / Easter"
    return "Ordinary Time"

season_text = season(datetime.now().month)
today_feast = feasts.get(today_mmdd)

# =========================
# ROOT
# =========================
root = tk.Tk()
root.title("Seelos Rule of Life")
root.geometry("700x800")
root.configure(bg=BG)

# =========================
# HEADER
# =========================
header = tk.Frame(root, bg=CARD, bd=2, relief="ridge")
header.pack(pady=10, fill="x")

tk.Label(
    header,
    text="Blessed Francis Xavier Seelos",
    font=("Times", 20, "bold"),
    bg=CARD,
    fg=ACCENT
).pack()

tk.Label(
    header,
    text=today_display,
    font=("Times", 14),
    bg=CARD,
    fg=TEXT
).pack()

# =========================
# CALENDAR
# =========================
calendar = tk.Frame(root, bg=CARD, bd=2, relief="ridge")
calendar.pack(pady=10, fill="x")

tk.Label(calendar, text=f"Season: {season_text}", bg=CARD, fg=TEXT).pack()

if today_feast:
    tk.Label(calendar, text=f"Feast: {today_feast}", bg=CARD, fg=ACCENT).pack()

# =========================
# SAINT
# =========================
saint_frame = tk.Frame(root, bg=CARD, bd=2, relief="ridge")
saint_frame.pack(pady=10, fill="x")

tk.Label(
    saint_frame,
    text="Saint of the Month",
    font=("Times", 16, "bold"),
    bg=CARD,
    fg=ACCENT
).pack()

tk.Label(
    saint_frame,
    text=saint["name"],
    font=("Times", 15),
    bg=CARD,
    fg=TEXT
).pack()

tk.Label(
    saint_frame,
    text="\n".join("• " + v for v in saint["virtues"]),
    bg=CARD,
    fg=TEXT
).pack()

# =========================
# DASHBOARD
# =========================
dashboard = tk.Frame(root, bg=CARD, bd=2, relief="ridge")
dashboard.pack(pady=10, fill="x")

dash_label = tk.Label(dashboard, text="Today: 0%", bg=CARD, fg=TEXT)
dash_label.pack()

bar = tk.Label(dashboard, font=("Courier", 16), bg=CARD, fg=GOLD)
bar.pack()

def update_dashboard():
    completed = sum(v.get() for v in checkbox_vars.values())
    percent = int((completed / len(tasks)) * 100)

    dash_label.config(text=f"Today: {percent}%")
    bar.config(text="█" * (percent // 10) + "░" * (10 - percent // 10))

# =========================
# STREAKS
# =========================
streak_frame = tk.Frame(root, bg=CARD, bd=2, relief="ridge")
streak_frame.pack(pady=10, fill="x")

tk.Label(
    streak_frame,
    text="Streaks",
    font=("Times", 16, "bold"),
    bg=CARD,
    fg=ACCENT
).pack()

rosary = tk.Label(streak_frame, bg=CARD, fg=TEXT)
mass = tk.Label(streak_frame, bg=CARD, fg=TEXT)
reading = tk.Label(streak_frame, bg=CARD, fg=TEXT)

rosary.pack()
mass.pack()
reading.pack()

def update_streak_display():
    rosary.config(text=f"Rosary: 🔥 {settings['streaks']['rosary']}")
    mass.config(text=f"Mass: 🔥 {settings['streaks']['mass']}")
    reading.config(text=f"Reading: 🔥 {settings['streaks']['reading']}")

# =========================
# CHECKLIST
# =========================
checklist = tk.Frame(root, bg=CARD, bd=2, relief="ridge")
checklist.pack(pady=10, fill="x")

def save_state():
    data[today_date] = {}

    for t, v in checkbox_vars.items():
        data[today_date][t] = v.get()

def on_close():
    save_state()

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

for t in tasks:
    v = tk.BooleanVar()

    cb = tk.Checkbutton(
        checklist,
        text=t,
        variable=v,
        bg=CARD,
        fg=TEXT,
        selectcolor=GOLD,
        activebackground=CARD,
        command=update_dashboard
    )
    cb.pack(anchor="w")

    checkbox_vars[t] = v

# =========================
# RESTORE STATE
# =========================
if today_date in data:
    saved = data[today_date]
    for t, v in checkbox_vars.items():
        if t in saved:
            v.set(saved[t])

# =========================
# INIT
# =========================
update_streaks()
update_dashboard()
update_streak_display()

# =========================
# START
# =========================
root.mainloop()