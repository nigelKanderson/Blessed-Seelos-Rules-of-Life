import tkinter as tk
from datetime import datetime
import random

root = tk.Tk()

root.title("Seelos Rule of Life")
root.geometry("700x800")

today = datetime.now()
today_string = today.strftime("%B %d, %Y")

header_frame = tk.Frame(root)

header_frame.pack(pady=20)


title = tk.Label(
    header_frame,
    text="Blessed Francis Xavier Seelos\nPractical Guide to Holiness",
    font=("Times",20)
)

title.pack()

date_label = tk.Label(
    header_frame,
    text=today_string,
    font=("Times",14)
)

date_label.pack()

quote_label = tk.Label(
    header_frame,
    text='"The Lord knows best what is good for us."',
    font=("Times",12),
    wraplength=500
)

quote_label.pack(pady=10)

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

saints = [

    {
        "name": "St. Joseph",
        "virtues": [
            "Obedience",
            "Silence",
            "Faithfulness"
        ]
    },

    {
        "name": "St. Francis de Sales",
        "virtues": [
            "Gentleness",
            "Patience",
            "Charity"
        ]
    },

    {
        "name": "St. Thérèse of Lisieux",
        "virtues": [
            "Humility",
            "Trust",
            "Love"
        ]
    },

    {
        "name": "St. Teresa of Calcutta",
        "virtues": [
            "Compassion",
            "Service",
            "Perseverance"
        ]
    }

]

saint = random.choice(saints)

saint_frame = tk.Frame(
    root,
    relief="ridge",
    borderwidth=3
)

saint_frame.pack(
    pady=20,
    padx=20,
    fill="x"
)

saint_title = tk.Label(
    saint_frame,
    text="Saint of the Month",
    font=("Times",16,"bold")
)

saint_title.pack(pady=5)

saint_name = tk.Label(
    saint_frame,
    text=saint["name"],
    font=("Times",15)
)

saint_name.pack()

virtue_text = ""

for virtue in saint["virtues"]:
    virtue_text += "• " + virtue + "\n"

virtue_label = tk.Label(
    saint_frame,
    text=virtue_text,
    font=("Times",13),
    justify="left"
)

virtue_label.pack(pady=10)

checklist_frame = tk.Frame(root)

checklist_frame.pack(pady=20)

for task in tasks:

    var = tk.BooleanVar()

    checkbox = tk.Checkbutton(
        checklist_frame,
        text=task,
        variable=var,
        font=("Times",13)
    )

    checkbox.pack(anchor="w")

root.mainloop()