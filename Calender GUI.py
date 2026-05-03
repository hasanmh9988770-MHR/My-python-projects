import os
import tkinter as tk
from tkinter import simpledialog
import threading
import uuid
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import calendar
from dotenv import load_dotenv
import dateparser
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. CONFIG & FIREBASE ---
load_dotenv()
FB_KEY_PATH = os.getenv("FIREBASE_KEY_PATH", "serviceAccountKey.json")
PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "calender-gui-6d81d")

db = None
if os.path.exists(FB_KEY_PATH):
    try:
        cred = credentials.Certificate(FB_KEY_PATH)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print(f"✅ Connected to Firebase: {PROJECT_ID}")
    except Exception as e:
        print(f"❌ Firebase Error: {e}")

# --- 2. THEME ---
BG_COLOR = "#000000"
SIDEBAR_COLOR = "#1C1C1E"
CARD_COLOR = "#2C2C2E"
ACCENT_BLUE = "#0A84FF"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#8E8E93"

FONT_SANS = (".AppleSystemUIFont", 13)
FONT_BOLD = (".AppleSystemUIFont", 18, "bold")
FONT_GRID = (".AppleSystemUIFont", 15)
FONT_HEADER = (".AppleSystemUIFont", 48, "bold")

engine = pyttsx3.init()


def speak(text):
    threading.Thread(target=lambda: (engine.say(text), engine.runAndWait()), daemon=True).start()


class GodLevelCalendar:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligence")
        self.root.geometry("1250x850")
        self.root.configure(bg=BG_COLOR)

        self.events = {}  # Task storage
        self.view_date = datetime.now()
        self.grid_month = self.view_date.month
        self.grid_year = self.view_date.year

        self.setup_ui()
        self.refresh_all()
        speak("Systems active.")

    def setup_ui(self):
        # --- SIDEBAR ---
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR_COLOR, width=320)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="Calendar", bg=SIDEBAR_COLOR,
                 fg=TEXT_PRIMARY, font=FONT_BOLD).pack(pady=(60, 20), padx=30, anchor="w")

        # Grid Container
        self.grid_container = tk.Frame(self.sidebar, bg=SIDEBAR_COLOR)
        self.grid_container.pack(pady=10, padx=20, fill="x")

        # Month Nav
        nav_f = tk.Frame(self.sidebar, bg=SIDEBAR_COLOR)
        nav_f.pack(fill="x", padx=30, pady=5)

        btn_prev = tk.Label(nav_f, text="<", fg=ACCENT_BLUE, bg=SIDEBAR_COLOR, font=FONT_BOLD, cursor="pointinghand")
        btn_prev.pack(side="left")
        btn_prev.bind("<Button-1>", lambda e: self.change_month(-1))

        self.month_label = tk.Label(nav_f, text="", bg=SIDEBAR_COLOR, fg=TEXT_PRIMARY, font=FONT_SANS)
        self.month_label.pack(side="left", expand=True)

        btn_next = tk.Label(nav_f, text=">", fg=ACCENT_BLUE, bg=SIDEBAR_COLOR, font=FONT_BOLD, cursor="pointinghand")
        btn_next.pack(side="right")
        btn_next.bind("<Button-1>", lambda e: self.change_month(1))

        tk.Frame(self.sidebar, bg="#333333", height=1).pack(fill="x", padx=30, pady=20)

        # Action Buttons
        self.create_mac_button("🎤  Voice Command", self.voice_command, ACCENT_BLUE)
        self.create_mac_button("⌨️  Type Task", self.ai_popup, "#3A3A3C")
        self.create_mac_button("🔘  View Today", self.reset_to_today, "#3A3A3C")
        self.create_mac_button("📂  Show All Tasks", lambda: self.render_agenda(show_all=True), "#3A3A3C")

        # --- MAIN AREA ---
        self.main = tk.Frame(self.root, bg=BG_COLOR)
        self.main.pack(side="right", expand=True, fill="both", padx=60)

        self.date_display = tk.Label(self.main, text="", bg=BG_COLOR, fg=TEXT_PRIMARY, font=FONT_HEADER)
        self.date_display.pack(pady=(80, 20), anchor="w")

        tk.Label(self.main, text="UPCOMING AGENDA", bg=BG_COLOR, fg=ACCENT_BLUE,
                 font=(".AppleSystemUIFont", 11, "bold")).pack(anchor="w")

        self.canvas = tk.Canvas(self.main, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, pady=20)

    def create_mac_button(self, text, cmd, color):
        btn = tk.Label(self.sidebar, text=text, bg=color, fg="white",
                       font=FONT_SANS, pady=12, cursor="pointinghand")
        btn.pack(fill="x", padx=30, pady=5)
        btn.bind("<Button-1>", lambda e: cmd())

    def change_month(self, delta):
        self.grid_month += delta
        if self.grid_month > 12:
            self.grid_month = 1; self.grid_year += 1
        elif self.grid_month < 1:
            self.grid_month = 12; self.grid_year -= 1
        self.render_month_grid()

    def render_month_grid(self):
        for w in self.grid_container.winfo_children(): w.destroy()
        self.month_label.config(text=f"{calendar.month_name[self.grid_month]} {self.grid_year}")

        cal = calendar.monthcalendar(self.grid_year, self.grid_month)
        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day == 0: continue
                is_sel = (
                            day == self.view_date.day and self.grid_month == self.view_date.month and self.grid_year == self.view_date.year)

                lbl = tk.Label(self.grid_container, text=str(day),
                               bg=ACCENT_BLUE if is_sel else SIDEBAR_COLOR,
                               fg="white", font=FONT_GRID, width=3, height=1, cursor="pointinghand")
                lbl.grid(row=r, column=c, padx=2, pady=2)
                lbl.bind("<Button-1>", lambda e, d=day: self.select_day(d))

    def select_day(self, day):
        self.view_date = datetime(self.grid_year, self.grid_month, day)
        self.refresh_all()

    def refresh_all(self):
        self.date_display.config(text=self.view_date.strftime("%B %d"))
        self.render_month_grid()
        self.render_agenda()

    def render_agenda(self, show_all=False):
        self.canvas.delete("all")
        if show_all:
            evs = list(self.events.values())
            self.date_display.config(text="All Tasks")
        else:
            target = self.view_date.strftime("%Y-%m-%d")
            evs = [e for e in self.events.values() if e["datetime"].strftime("%Y-%m-%d") == target]
            self.date_display.config(text=self.view_date.strftime("%B %d"))

        evs.sort(key=lambda x: x["datetime"])

        if not evs:
            self.canvas.create_text(0, 40, text="No Tasks Scheduled.", fill=TEXT_SECONDARY, font=FONT_SANS, anchor="w")
            return

        y = 10
        for e in evs:
            self.canvas.create_rectangle(0, y, 750, y + 85, fill=CARD_COLOR, outline="")
            self.canvas.create_rectangle(0, y, 5, y + 85, fill=ACCENT_BLUE, outline="")
            time_txt = e["datetime"].strftime("%b %d, %I:%M %p") if show_all else e["datetime"].strftime("%I:%M %p")
            self.canvas.create_text(25, y + 25, text=e["title"].upper(), fill=TEXT_PRIMARY, font=FONT_BOLD, anchor="w")
            self.canvas.create_text(25, y + 55, text=time_txt, fill=ACCENT_BLUE, font=FONT_SANS, anchor="w")
            y += 100

    def process_ai(self, text):
        parsed = dateparser.parse(text, settings={'PREFER_DATES_FROM': 'future'})
        if parsed:
            eid = str(uuid.uuid4())
            title = text.lower().replace("remind me", "").replace("at", "").replace("add", "").strip().title()
            event_data = {"title": title or "New Task", "datetime": parsed}
            self.events[eid] = event_data

            if db:
                threading.Thread(target=lambda: db.collection("tasks").document(eid).set({
                    "title": event_data["title"],
                    "time": event_data["datetime"].isoformat()
                }), daemon=True).start()

            self.view_date = parsed
            self.grid_month, self.grid_year = parsed.month, parsed.year
            self.refresh_all()
            speak(f"Saved {title}")
        else:
            speak("Time not recognized.")

    def voice_command(self):
        def _listen():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                try:
                    speak("Listening...")
                    audio = r.listen(source, timeout=5)
                    query = r.recognize_google(audio)
                    self.root.after(0, lambda: self.process_ai(query))
                except:
                    speak("Missed that.")

        threading.Thread(target=_listen, daemon=True).start()

    def ai_popup(self):
        cmd = simpledialog.askstring("Siri", "What is the task?")
        if cmd: self.process_ai(cmd)

    def reset_to_today(self):
        self.view_date = datetime.now()
        self.grid_month, self.grid_year = self.view_date.month, self.view_date.year
        self.refresh_all()


if __name__ == "__main__":
    root = tk.Tk()
    root.tk.call('tk', 'scaling', 2.0)
    app = GodLevelCalendar(root)
    root.mainloop()