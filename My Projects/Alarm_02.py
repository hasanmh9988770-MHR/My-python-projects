import tkinter as tk
from tkinter import messagebox, filedialog
import datetime
import os
import pygame


class ProAlarmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MHR PRO MODE ALARM 🔔")
        self.root.geometry("480x750")
        self.root.configure(bg="#0a0e1a")

        # Initialize Pygame Mixer
        pygame.mixer.init()

        self.alarm_time = None
        self.music_path = None
        self.is_ringing = False
        self.mission_mode = False

        self.create_widgets()
        self.update_clock()

    def create_widgets(self):
        # Header & Clock
        tk.Label(self.root, text="Alarm", font=("Arial", 24, "bold"), fg="white", bg="#0a0e1a").pack(pady=10)

        self.clock_label = tk.Label(self.root, text="00:00:00 PM", font=("Arial", 40, "bold"), fg="white", bg="#0a0e1a")
        self.clock_label.pack(pady=20)

        # Time Pickers
        time_frame = tk.Frame(self.root, bg="#0a0e1a")
        time_frame.pack(pady=10)

        self.hour_val = tk.StringVar(value="01")
        self.min_val = tk.StringVar(value="30")
        self.am_pm_val = tk.StringVar(value="PM")

        tk.Spinbox(time_frame, from_=1, to=12, textvariable=self.hour_val, width=3, font=("Arial", 18)).grid(row=0,
                                                                                                             column=0)
        tk.Label(time_frame, text=":", fg="white", bg="#0a0e1a", font=("Arial", 18)).grid(row=0, column=1)
        tk.Spinbox(time_frame, from_=0, to=59, textvariable=self.min_val, width=3, font=("Arial", 18),
                   format="%02.0f").grid(row=0, column=2)
        tk.OptionMenu(time_frame, self.am_pm_val, "AM", "PM").grid(row=0, column=3, padx=10)

        # Main Buttons
        tk.Button(self.root, text="Add Alarm", command=self.set_alarm, width=25, bg="white", fg="black",
                  font=("Arial", 12, "bold"), highlightbackground="#0a0e1a").pack(pady=15)

        self.status_label = tk.Label(self.root, text="⏰ No Alarm Set", fg="#888", bg="#0a0e1a", font=("Arial", 12))
        self.status_label.pack(pady=5)

        tk.Button(self.root, text="Select Sound", command=self.select_sound, width=25, bg="white", fg="black",
                  highlightbackground="#0a0e1a").pack(pady=10)
        self.sound_label = tk.Label(self.root, text="No sound selected", fg="#888", bg="#0a0e1a", font=("Arial", 10),
                                    wraplength=350)
        self.sound_label.pack()

        tk.Button(self.root, text="Mission Mode", command=self.toggle_mission, width=25, bg="white", fg="black",
                  highlightbackground="#0a0e1a").pack(pady=10)
        self.mission_label = tk.Label(self.root, text="Mission: OFF", fg="#888", bg="#0a0e1a")
        self.mission_label.pack()

        # CONTROL SECTION
        control_frame = tk.Frame(self.root, bg="#0a0e1a")
        control_frame.pack(pady=30)

        # Using standard button calls to ensure they don't get stuck
        self.stop_btn = tk.Button(control_frame, text="STOP", command=self.stop_alarm, width=10, bg="white", fg="black",
                                  highlightbackground="#0a0e1a")
        self.stop_btn.grid(row=0, column=0, padx=5)

        self.remove_btn = tk.Button(control_frame, text="Remove", command=self.remove_alarm, width=10, bg="white",
                                    fg="black", highlightbackground="#0a0e1a")
        self.remove_btn.grid(row=0, column=1, padx=5)

        self.snooze_btn = tk.Button(control_frame, text="Snooze", command=self.snooze_alarm, width=10, bg="white",
                                    fg="black", highlightbackground="#0a0e1a")
        self.snooze_btn.grid(row=0, column=2, padx=5)

        tk.Label(self.root, text="🔥 WAKE UP NOW", fg="#ff4500", bg="#0a0e1a", font=("Arial", 10, "bold")).pack(
            side="bottom", pady=20)

    def update_clock(self):
        now = datetime.datetime.now()
        current_time_str = now.strftime("%I:%M %p")
        self.clock_label.config(text=now.strftime("%I:%M:%S %p"))

        # Ring only if the time matches AND we aren't already ringing
        if self.alarm_time == current_time_str and not self.is_ringing:
            self.ring_alarm()

        self.root.after(1000, self.update_clock)

    def set_alarm(self):
        self.alarm_time = f"{int(self.hour_val.get()):02}:{int(self.min_val.get()):02} {self.am_pm_val.get()}"
        self.status_label.config(text=f"⏰ {self.alarm_time}", fg="#00ff00")
        self.is_ringing = False  # Reset ringing state when setting a new one

    def select_sound(self):
        file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file:
            self.music_path = file
            self.sound_label.config(text=os.path.basename(file))

    def toggle_mission(self):
        self.mission_mode = not self.mission_mode
        state = "ON" if self.mission_mode else "OFF"
        self.mission_label.config(text=f"Mission: {state}", fg="cyan" if self.mission_mode else "#888")

    def ring_alarm(self):
        self.is_ringing = True
        self.stop_btn.config(text="STOP NOW", fg="red")
        if self.music_path:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play(-1)
        else:
            messagebox.showwarning("Alarm!", "WAKE UP!")

    def stop_alarm(self):
        """Force stops the mixer and resets the UI state."""
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.is_ringing = False

        # Reset Button Appearance
        self.stop_btn.config(text="STOP", fg="black")

        # If alarm was active, mark it as stopped
        if self.alarm_time:
            self.status_label.config(text=f"⏰ Stopped: {self.alarm_time}", fg="#888")

        # Crucial for Mac UI update
        self.root.update()

    def remove_alarm(self):
        self.stop_alarm()
        self.alarm_time = None
        self.status_label.config(text="⏰ No Alarm Set", fg="#888")

    def snooze_alarm(self):
        if self.is_ringing:
            self.stop_alarm()
            now = datetime.datetime.now() + datetime.timedelta(minutes=5)
            self.alarm_time = now.strftime("%I:%M %p")
            self.status_label.config(text=f"⏰ Snoozed: {self.alarm_time}", fg="yellow")


if __name__ == "__main__":
    root = tk.Tk()
    app = ProAlarmApp(root)
    root.mainloop()

### CREATED BY MHR
### PYTHON 3.14 VERSION USED