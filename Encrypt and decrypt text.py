import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import base64
import secrets
import string
import re

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256


# =========================
# CRYPTO CONFIG
# =========================
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
ITERATIONS = 200_000


# =========================
# KEY DERIVATION
# =========================
def derive_key(password, salt):
    return PBKDF2(
        password,
        salt,
        dkLen=KEY_SIZE,
        count=ITERATIONS,
        hmac_hash_module=SHA256
    )


# =========================
# ENCRYPT / DECRYPT CORE
# =========================
def encrypt(data: bytes, password: str) -> str:
    salt = get_random_bytes(SALT_SIZE)
    key = derive_key(password, salt)

    nonce = get_random_bytes(NONCE_SIZE)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    ciphertext, tag = cipher.encrypt_and_digest(data)

    return base64.b64encode(salt + nonce + tag + ciphertext).decode()


def decrypt(data: str, password: str) -> bytes:
    raw = base64.b64decode(data)

    salt = raw[:SALT_SIZE]
    nonce = raw[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    tag = raw[SALT_SIZE + NONCE_SIZE:SALT_SIZE + NONCE_SIZE + 16]
    ciphertext = raw[SALT_SIZE + NONCE_SIZE + 16:]

    key = derive_key(password, salt)

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


# =========================
# AI SECURITY ENGINE
# =========================
def password_strength(pwd):
    score = 0

    if len(pwd) >= 12:
        score += 2
    elif len(pwd) >= 8:
        score += 1

    if re.search(r"[A-Z]", pwd):
        score += 1
    if re.search(r"[a-z]", pwd):
        score += 1
    if re.search(r"[0-9]", pwd):
        score += 1
    if re.search(r"[!@#$%^&*()_+]", pwd):
        score += 1

    if score <= 2:
        return "WEAK 🔴"
    elif score <= 4:
        return "MEDIUM 🟡"
    else:
        return "STRONG 🟢"


def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    return ''.join(secrets.choice(chars) for _ in range(length))


# =========================
# FOLDER ENCRYPTION
# =========================
def encrypt_folder(folder, password):
    for root, _, files in os.walk(folder):
        for f in files:
            path = os.path.join(root, f)

            try:
                with open(path, "rb") as file:
                    data = file.read()

                enc = encrypt(data, password)

                with open(path + ".enc", "w") as file:
                    file.write(enc)

            except:
                pass


def decrypt_folder(folder, password):
    for root, _, files in os.walk(folder):
        for f in files:
            if not f.endswith(".enc"):
                continue

            path = os.path.join(root, f)

            try:
                with open(path, "r") as file:
                    data = file.read()

                dec = decrypt(data, password)

                out = path.replace(".enc", "")

                with open(out, "wb") as file:
                    file.write(dec)

            except:
                pass


# =========================
# STEALTH MODE
# =========================
class StealthMode:
    def __init__(self, root, vault):
        self.root = root
        self.vault = vault

        self.fake = tk.Toplevel(root)
        self.fake.title("Calculator")
        self.fake.geometry("300x400")

        self.entry = tk.Entry(self.fake, font=("Arial", 16))
        self.entry.pack(pady=20)

        tk.Button(self.fake, text="=", command=self.calc).pack()

        root.bind("<Control-Shift-v>", self.open_vault)
        root.bind("<Escape>", self.hide_all)

    def calc(self):
        try:
            res = eval(self.entry.get())
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(res))
        except:
            self.entry.insert(0, "Error")

    def open_vault(self, event=None):
        self.vault.root.deiconify()
        self.fake.withdraw()

    def hide_all(self, event=None):
        self.vault.root.withdraw()
        self.fake.withdraw()


# =========================
# VAULT APP
# =========================
class VaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PRO VAULT ULTRA 🔐")
        self.root.geometry("800x600")

        self.data = {}
        self.file = "vault.enc"

        self.build_ui()

        StealthMode(root, self)

    def build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        self.tab1 = ttk.Frame(notebook)
        self.tab2 = ttk.Frame(notebook)
        self.tab3 = ttk.Frame(notebook)

        notebook.add(self.tab1, text="🔐 Vault")
        notebook.add(self.tab2, text="🔑 Generator")
        notebook.add(self.tab3, text="📁 Files")

        self.vault_ui()
        self.generator_ui()
        self.file_ui()

    # ================= VAULT =================
    def vault_ui(self):
        tk.Label(self.tab1, text="Master Password").pack()
        self.master = tk.Entry(self.tab1, show="*")
        self.master.pack()

        tk.Button(self.tab1, text="Load Vault", command=self.load).pack()

        tk.Label(self.tab1, text="Key").pack()
        self.k = tk.Entry(self.tab1)
        self.k.pack()

        tk.Label(self.tab1, text="Value").pack()
        self.v = tk.Entry(self.tab1)
        self.v.pack()

        tk.Button(self.tab1, text="Add", command=self.add).pack()
        tk.Button(self.tab1, text="Save", command=self.save).pack()

        self.out = tk.Text(self.tab1)
        self.out.pack(fill="both", expand=True)

    def add(self):
        self.data[self.k.get()] = self.v.get()
        self.out.insert(tk.END, f"[+] {self.k.get()}\n")

    def save(self):
        raw = json.dumps(self.data).encode()
        enc = encrypt(raw, self.master.get())

        with open(self.file, "w") as f:
            f.write(enc)

        messagebox.showinfo("Saved", "Vault secured!")

    def load(self):
        try:
            with open(self.file, "r") as f:
                enc = f.read()

            raw = decrypt(enc, self.master.get())
            self.data = json.loads(raw.decode())

            self.out.insert(tk.END, "[✔] Loaded\n")

        except:
            messagebox.showerror("Error", "Wrong password")

    # ================= GENERATOR =================
    def generator_ui(self):
        tk.Label(self.tab2, text="Length").pack()
        self.len = tk.Entry(self.tab2)
        self.len.insert(0, "16")
        self.len.pack()

        tk.Button(self.tab2, text="Generate", command=self.gen).pack()

        self.passout = tk.Entry(self.tab2, width=40)
        self.passout.pack()

        tk.Button(self.tab2, text="Copy", command=self.copy).pack()
        tk.Button(self.tab2, text="Check Strength", command=self.check).pack()

    def gen(self):
        self.passout.delete(0, tk.END)
        self.passout.insert(0, generate_password(int(self.len.get())))

    def copy(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.passout.get())

    def check(self):
        result = password_strength(self.passout.get())
        messagebox.showinfo("Strength", result)

    # ================= FILES =================
    def file_ui(self):
        tk.Button(self.tab3, text="Encrypt File", command=self.enc_file).pack()
        tk.Button(self.tab3, text="Decrypt File", command=self.dec_file).pack()
        tk.Button(self.tab3, text="Encrypt Folder", command=self.enc_folder).pack()
        tk.Button(self.tab3, text="Decrypt Folder", command=self.dec_folder).pack()

    def enc_file(self):
        path = filedialog.askopenfilename()
        pwd = self.master.get()

        with open(path, "rb") as f:
            data = f.read()

        enc = encrypt(data, pwd)

        with open(path + ".enc", "w") as f:
            f.write(enc)

    def dec_file(self):
        path = filedialog.askopenfilename()
        pwd = self.master.get()

        with open(path, "r") as f:
            data = f.read()

        dec = decrypt(data, pwd)

        out = path.replace(".enc", "")

        with open(out, "wb") as f:
            f.write(dec)

    def enc_folder(self):
        folder = filedialog.askdirectory()
        encrypt_folder(folder, self.master.get())

    def dec_folder(self):
        folder = filedialog.askdirectory()
        decrypt_folder(folder, self.master.get())


# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = VaultApp(root)
    root.mainloop()