import tkinter as tk
from tkinter import messagebox
import datetime
import time
import os
from threading import Thread


def start_alarm_thread():
    # Show a message so we know the button was clicked
    print("--- Alarm Thread Started ---")
    t1 = Thread(target=alarm_logic, daemon=True)
    t1.start()


def alarm_logic():
    while True:
        # Get the time from the dropdowns
        set_alarm_time = f"{hour.get()}:{minute.get()}:{second.get()}"

        # Wait 1 second
        time.sleep(1)

        # Get current system time
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        # MONITOR: This shows you exactly what the code is doing in the PyCharm 'Run' tab
        print(f"Checking... Current: {current_time} | Target: {set_alarm_time}")

        if current_time == set_alarm_time:
            print("!!! MATCH FOUND !!!")
            # Using 'say' as a backup because 'afplay' can be silent if volume is low
            os.system('say "Time to wake up"')
            os.system('afplay /System/Library/Sounds/Ping.aiff')
            messagebox.showinfo("Alarm", f"It is {set_alarm_time}!\nTime to Wake up!")
            break


# GUI Setup
root = tk.Tk()
root.title("Python Alarm Clock")
root.geometry("400x300")

tk.Label(root, text="Alarm Clock", font=("Helvetica 20 bold"), fg="red").pack(pady=10)
tk.Label(root, text="Set Time (24h Format)", font=("Helvetica 12")).pack()

frame = tk.Frame(root)
frame.pack(pady=10)

# Time Selection Lists
hours = [f"{i:02d}" for i in range(24)]
minutes = [f"{i:02d}" for i in range(60)]
seconds = [f"{i:02d}" for i in range(60)]

hour = tk.StringVar(root, value=datetime.datetime.now().strftime("%H"))
tk.OptionMenu(frame, hour, *hours).pack(side=tk.LEFT)

minute = tk.StringVar(root, value=datetime.datetime.now().strftime("%M"))
tk.OptionMenu(frame, minute, *minutes).pack(side=tk.LEFT)

second = tk.StringVar(root, value="00")
tk.OptionMenu(frame, second, *seconds).pack(side=tk.LEFT)

tk.Button(root, text="Set Alarm", font=("Helvetica 15"), command=start_alarm_thread, bg="green").pack(pady=20)

root.mainloop()