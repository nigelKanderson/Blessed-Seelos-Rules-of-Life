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
# FILES
# =========================
SAVE_DIR = "save"
SAVE_FILE = os.path.join(SAVE_DIR, "daily_log.json")
SETTINGS_FILE = os.path.join(SAVE_DIR, "settings.json")

os.makedirs(SAVE_DIR, exist_ok=True)

# =========================
# SAFE JSON LOADER
# =========================
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

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

# =========================
# STREAK SYSTEM INIT
# =========================
if "streaks" not in settings:
    settings["streaks"] = {
        "rosary": 0,
        "mass": 0,
        "reading": 0
    }

if "last_streak_date" not in settings:
    settings["last_streak_date"] = today_date

streak_map = {
    "Go to Mass with deepest devotion": "mass",
    "Pray the Rosary": "rosary",
    "Spiritual reading": "reading"
}

def update_streaks():
    last_date = settings.get("last_streak_date")

    if last_date == today_date:
        return

    previous = data.get(last_date, {})

    for task, category in streak_map.items():
        if previous.get(task, False):
            settings["streaks"][category] += 1
        else:
            settings["streaks"][category] = 0

    settings["last_streak_date"] = today_date

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

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

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

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
    "08-15": "Assumption of Mary",
    "10-02": "Guardian Angels",
    "11-01": "All Saints",
    "12-08": "Immaculate Conception",
    "12-25": "Nativity of the Lord"
}

def get_season(month):
    if month in [11, 12]:
        return "Advent / Transition"
    elif month in [3, 4]:
        return "Lent / Easter"
    else:
        return "Ordinary Time"

season_text = get_season(datetime.now().month)
today_feast = feasts.get(today_mmdd)

# =========================
# TKINTER ROOT
# =========================
root = tk.Tk()
root.title("Seelos Rule of Life")
root.geometry("700x800")

# =========================
# HEADER
# =========================
header = tk.Frame(root)
header.pack(pady=10)

tk.Label(header, text="Blessed Francis Xavier Seelos", font=("Times", 20)).pack()
tk.Label(header, text=today_display, font=("Times", 14)).pack()

# =========================
# CALENDAR UI
# =========================
calendar_frame = tk.Frame(root)
calendar_frame.pack(pady=10)

tk.Label(calendar_frame, text=f"Season: {season_text}", font=("Times", 13, "italic")).pack()

if today_feast:
    tk.Label(calendar_frame, text=f"Feast: {today_feast}", font=("Times", 13, "bold")).pack()

# =========================
# SAINT UI
# =========================
saint_frame = tk.Frame(root, relief="ridge", borderwidth=3)
saint_frame.pack(pady=10, padx=10, fill="x")

tk.Label(saint_frame, text="Saint of the Month", font=("Times", 16, "bold")).pack()
tk.Label(saint_frame, text=saint["name"], font=("Times", 15)).pack()

tk.Label(
    saint_frame,
    text="\n".join(["• " + v for v in saint["virtues"]]),
    font=("Times", 13)
).pack()

# =========================
# DASHBOARD
# =========================
dashboard = tk.Frame(root)
dashboard.pack(pady=10)

dashboard_label = tk.Label(dashboard, text="Today's Completion: 0%", font=("Times", 14, "bold"))
dashboard_label.pack()

progress_bar = tk.Label(dashboard, text="□□□□□□□□□□", font=("Courier", 16))
progress_bar.pack()

def update_dashboard():
    completed = sum(var.get() for var in checkbox_vars.values())
    percent = int((completed / len(tasks)) * 100)

    dashboard_label.config(text=f"Today's Completion: {percent}%")

    filled = percent // 10
    progress_bar.config(text="■" * filled + "□" * (10 - filled))

# =========================
# STREAK UI
# =========================
streak_frame = tk.Frame(root)
streak_frame.pack(pady=10)

tk.Label(streak_frame, text="Streaks", font=("Times", 16, "bold")).pack()

rosary_label = tk.Label(streak_frame, font=("Times", 13))
rosary_label.pack()

mass_label = tk.Label(streak_frame, font=("Times", 13))
mass_label.pack()

reading_label = tk.Label(streak_frame, font=("Times", 13))
reading_label.pack()

def update_streak_display():
    rosary_label.config(text=f"Rosary: 🔥 {settings['streaks']['rosary']} days")
    mass_label.config(text=f"Mass: 🔥 {settings['streaks']['mass']} days")
    reading_label.config(text=f"Reading: 🔥 {settings['streaks']['reading']} days")

# =========================
# CHECKLIST
# =========================
checklist = tk.Frame(root)
checklist.pack(pady=10)

def save_state():
    data[today_date] = {}

    for task, var in checkbox_vars.items():
        data[today_date][task] = var.get()

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def on_close():
    save_state()

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

for task in tasks:
    var = tk.BooleanVar()

    cb = tk.Checkbutton(
        checklist,
        text=task,
        variable=var,
        font=("Times", 13),
        command=update_dashboard
    )

    cb.pack(anchor="w")
    checkbox_vars[task] = var

# =========================
# RESTORE STATE
# =========================
if today_date in data:
    saved = data[today_date]
    for task, var in checkbox_vars.items():
        if task in saved:
            var.set(saved[task])

# =========================
# INIT SYSTEMS
# =========================
update_dashboard()
update_streaks()
update_streak_display()

# =========================
# SAVE BUTTON
# =========================
tk.Button(root, text="Save Today", command=save_state, font=("Times", 12)).pack(pady=10)

# =========================
# START
# =========================
root.mainloop()