import tkinter as tk
from tkinter import messagebox, filedialog, ttk, simpledialog
import datetime
import threading
import time
import os
import random
import pygame
import subprocess

pygame.mixer.init()

APP_TITLE = "🔥 FINAL GOD MODE ALARM ++"
BG = "#05070f"
CARD = "#111827"
FG = "#e5e7eb"
ACCENT = "#38bdf8"
DANGER = "#ef4444"
GLOW = "#22c55e"

AI_MESSAGES = [
    "Wake up. Your future self is judging you.",
    "Discipline beats motivation. Get up.",
    "You said you'd change. Today is proof.",
    "Stop scrolling. Start building.",
    "Pain today, power tomorrow.",
    "No excuses. Only execution.",
    "Your goals didn’t sleep. Why are you?"
]

class GodAlarm:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("520x820")
        self.root.configure(bg=BG)
        self.root.attributes("-topmost", True)

        self.alarms = []
        self.music_list = []
        self.ringing = False
        self.running = True

        self.drag_start = None
        self.passcode = None

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 12))
        self.style.configure("Accent.TButton", foreground="black", background=ACCENT)
        self.style.configure("Danger.TButton", foreground="white", background=DANGER)

        self.build_ui()
        self.clock_loop()
        self.engine()

        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.on_drag)

        self.root.protocol("WM_DELETE_WINDOW", self.block_close)

    # ================= UI =================
    def build_ui(self):

        tk.Label(self.root, text="📱 FINAL GOD MODE ++", bg=BG, fg=FG,
                 font=("Helvetica", 20, "bold")).pack(pady=10)

        self.clock = tk.Label(self.root, text="", bg=BG, fg=ACCENT,
                               font=("Helvetica", 40, "bold"))
        self.clock.pack(pady=10)

        card = tk.Frame(self.root, bg=CARD)
        card.pack(pady=10, padx=15, fill="x")

        self.hour = tk.StringVar(value="07")
        self.minute = tk.StringVar(value="30")
        self.ampm = tk.StringVar(value="AM")

        row = tk.Frame(card, bg=CARD)
        row.pack(pady=10)

        tk.Spinbox(row, from_=1, to=12, textvariable=self.hour, width=3, font=("Helvetica", 16)).pack(side="left")
        tk.Label(row, text=":", bg=CARD, fg=FG).pack(side="left")
        tk.Spinbox(row, from_=0, to=59, textvariable=self.minute, width=3, font=("Helvetica", 16)).pack(side="left")
        tk.OptionMenu(row, self.ampm, "AM", "PM").pack(side="left", padx=10)

        ttk.Button(card, text="➕ Add Alarm", style="Accent.TButton", command=self.add_alarm).pack(pady=10)

        self.listbox = tk.Listbox(self.root, bg=CARD, fg=FG, font=("Helvetica", 13), height=6)
        self.listbox.pack(pady=10, fill="x", padx=15)

        btns = tk.Frame(self.root, bg=BG)
        btns.pack(pady=10)

        ttk.Button(btns, text="STOP", style="Danger.TButton", command=self.stop_alarm).pack(side="left", padx=8)
        ttk.Button(btns, text="SNOOZE", style="Accent.TButton", command=self.snooze).pack(side="left", padx=8)
        ttk.Button(btns, text="DELETE", style="Danger.TButton", command=self.delete_alarm).pack(side="left", padx=8)

        ttk.Button(self.root, text="Select Sound", style="Accent.TButton", command=self.load_music).pack(pady=5)

        self.ai_label = tk.Label(self.root, text="AI: Idle", bg=BG, fg="#94a3b8", wraplength=450)
        self.ai_label.pack(pady=5)

        self.status = tk.Label(self.root, text="Idle", bg=BG, fg="#94a3b8")
        self.status.pack(pady=5)

    # ================= CLOCK =================
    def clock_loop(self):
        self.clock.config(text=datetime.datetime.now().strftime("%I:%M %p"))
        self.root.after(1000, self.clock_loop)

    # ================= ALARM =================
    def add_alarm(self):
        h = int(self.hour.get())
        m = int(self.minute.get())
        ap = self.ampm.get()

        if ap == "PM" and h != 12:
            h += 12
        if ap == "AM" and h == 12:
            h = 0

        self.alarms.append({"time": f"{h:02d}:{m:02d}", "active": True})
        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for a in self.alarms:
            h, m = map(int, a['time'].split(':'))
            ap = "AM"
            if h >= 12:
                ap = "PM"
            if h > 12:
                h -= 12
            if h == 0:
                h = 12
            self.listbox.insert(tk.END, f"⏰ {h:02d}:{m:02d} {ap}")

    # ================= DELETE ALARM =================
    def delete_alarm(self):
        try:
            selected = self.listbox.curselection()
            if not selected:
                messagebox.showinfo("Info", "Select an alarm to delete")
                return

            index = selected[0]
            del self.alarms[index]
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= ENGINE =================
    def engine(self):
        def loop():
            while self.running:
                now = datetime.datetime.now().strftime("%H:%M")
                for a in self.alarms:
                    if a['time'] == now and a['active']:
                        a['active'] = False
                        self.trigger()
                time.sleep(1)
        threading.Thread(target=loop, daemon=True).start()

    # ================= CINEMATIC ANIMATION =================
    def cinematic_flash(self):
        colors = ["#05070f", "#0f172a", "#1e293b", "#000000"]
        i = 0
        while self.ringing:
            self.root.configure(bg=colors[i % len(colors)])
            i += 1
            time.sleep(0.25)

    # ================= PASSCODE CHECK =================
    def ask_passcode(self):
        if self.passcode is None:
            self.passcode = simpledialog.askstring("Set Passcode", "Set alarm stop passcode:", show="*")
        code = simpledialog.askstring("Unlock Alarm", "Enter passcode:", show="*")
        return code == self.passcode

    # ================= TRIGGER =================
    def trigger(self):
        self.ringing = True
        self.status.config(text="🔥 WAKE UP MODE ACTIVE")

        self.show_ai_message()
        self.root.attributes("-fullscreen", True)

        threading.Thread(target=self.play_sound, daemon=True).start()
        threading.Thread(target=self.cinematic_flash, daemon=True).start()

    def show_ai_message(self):
        self.ai_label.config(text=f"🧠 AI: {random.choice(AI_MESSAGES)}")

    # ================= SOUND =================
    def load_music(self):
        folder = filedialog.askdirectory()
        if not folder:
            return
        self.music_list = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith((".mp3", ".wav"))]

    def play_sound(self):
        while self.ringing:
            try:
                if self.music_list:
                    f = random.choice(self.music_list)
                    pygame.mixer.music.load(f)
                    pygame.mixer.music.play()
                    time.sleep(4)
                else:
                    subprocess.call(["afplay", "/System/Library/Sounds/Glass.aiff"])
            except:
                pass

    # ================= STOP WITH PASSCODE =================
    def stop_alarm(self):
        if not self.ringing:
            return

        if self.ask_passcode():
            self.ringing = False
            pygame.mixer.music.stop()
            self.root.attributes("-fullscreen", False)
            self.status.config(text="Stopped")
        else:
            messagebox.showwarning("DENIED", "Wrong passcode!")

    def snooze(self):
        self.ringing = False
        new_time = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%H:%M")
        self.alarms.append({"time": new_time, "active": True})
        self.refresh()
        self.root.attributes("-fullscreen", False)

    # ================= SWIPE =================
    def start_drag(self, event):
        self.drag_start = event.y

    def on_drag(self, event):
        if self.ringing and self.drag_start and abs(event.y - self.drag_start) > 150:
            self.stop_alarm()

    # ================= SAFETY =================
    def block_close(self):
        if self.ringing:
            messagebox.showwarning("LOCKED", "Alarm active!")
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GodAlarm(root)
    root.mainloop()

### CREATED BY THE GOAT MHR ~ MEHEDI HASAN RABBY
### PYTHON 3.14 VERSION USED
