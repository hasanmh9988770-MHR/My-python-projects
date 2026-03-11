import tkinter as tk
from time import strftime

def change_theme(bg_color, fg_color):
    # Update the existing elements instead of creating new ones
    frame.config(bg=bg_color)
    lbl.config(background=bg_color, foreground=fg_color)

def update_time():
    string = strftime('%I:%M:%S %p')
    lbl.config(text=string)
    lbl.after(1000, update_time)

root = tk.Tk()
root.title("Digital-Clock")

# Set window size
canvas = tk.Canvas(root, height=140, width=400)
canvas.pack()

# Create elements ONCE
frame = tk.Frame(root, bg='#22478a')
frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

lbl = tk.Label(frame, font=('calibri', 40, 'bold'), background='#22478a', foreground='black')
lbl.pack(expand=True)

# Menu Bar setup
menubar = tk.Menu(root)
theme_menu = tk.Menu(menubar, tearoff=0)

# Commands now just change colors
theme_menu.add_command(label="Light", command=lambda: change_theme("white", "black"))
theme_menu.add_command(label="Dark", command=lambda: change_theme("#22478a", "white"))

menubar.add_cascade(label="Theme", menu=theme_menu)
root.config(menu=menubar)

# Start the clock and the app
update_time()
root.mainloop()