import customtkinter as ctk
from tkinter import simpledialog, messagebox

from hotel import Hotel
from user import User
import operations as op


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class App:
    def __init__(self):

        self.root = ctk.CTk()
        self.root.geometry("1100x650")
        self.root.title("Hotel Management System")

        # DATA
        self.hotels = [
            Hotel("H1", 4, "Bangalore", 5, 100),
            Hotel("H2", 5, "Bangalore", 5, 200),
            Hotel("H3", 6, "Mumbai", 3, 100)
        ]

        self.users = [
            User("U1", 2, 1000),
            User("U2", 3, 1200),
            User("U3", 4, 1100)
        ]

        self.login()

    # ---------------- LOGIN ----------------
    def login(self):

        self.login_frame = ctk.CTkFrame(self.root, width=350, height=250)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.login_frame,
            text="LOGIN",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        self.user = ctk.CTkEntry(self.login_frame, placeholder_text="Username")
        self.user.pack(pady=10)

        self.pwd = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.pwd.pack(pady=10)

        ctk.CTkButton(
            self.login_frame,
            text="Login",
            command=self.check_login
        ).pack(pady=20)

    def check_login(self):
        if self.user.get() == "admin" and self.pwd.get() == "****":
            self.login_frame.destroy()
            self.main_ui()
        else:
            messagebox.showerror("Error", "Wrong login!")

    # ---------------- MAIN UI ----------------
    def main_ui(self):

        self.sidebar = ctk.CTkFrame(self.root, width=220)
        self.sidebar.pack(side="left", fill="y")

        self.main = ctk.CTkFrame(self.root)
        self.main.pack(side="right", expand=True, fill="both")

        self.text = ctk.CTkTextbox(self.main, width=800, height=600)
        self.text.pack(pady=20)

        # SIDEBAR BUTTONS (FULL 8 FEATURES)
        buttons = [
            ("View Hotels", self.view_hotels),
            ("Sort Name", self.sort_name),
            ("Sort Rating", self.sort_rating),
            ("Sort Rooms", self.sort_rooms),
            ("Search City", self.search_city),
            ("Users", self.users_view),
            ("Book Hotel", self.book),
            ("Exit", self.root.quit)
        ]

        for name, cmd in buttons:
            ctk.CTkButton(self.sidebar, text=name, command=cmd).pack(pady=10)

        # Dark/Light toggle
        ctk.CTkSwitch(
            self.sidebar,
            text="Light Mode",
            command=self.toggle
        ).pack(pady=20)

    # ---------------- FEATURES ----------------
    def show(self, data):
        self.text.delete("0.0", "end")
        self.text.insert("end", data)

    def view_hotels(self):
        self.show(op.list_hotels(self.hotels))

    def sort_name(self):
        self.show(op.sort_by_name(self.hotels))

    def sort_rating(self):
        self.show(op.sort_by_rating(self.hotels))

    def sort_rooms(self):
        self.show(op.sort_by_rooms(self.hotels))

    def search_city(self):
        city = simpledialog.askstring("City", "Enter city:")
        if city:
            self.show(op.filter_city(city, self.hotels))

    def users_view(self):
        self.show(op.list_users(self.users))

    def book(self):
        name = simpledialog.askstring("Book", "Hotel name:")
        if name:
            msg = op.book_hotel(name, self.hotels)
            messagebox.showinfo("Booking", msg)

    def toggle(self):
        mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("light" if mode == "Dark" else "dark")

    def run(self):
        self.root.mainloop()