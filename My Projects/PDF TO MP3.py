import os
import asyncio
import PyPDF2
import edge_tts
import tkinter as tk
from tkinter import filedialog, messagebox

from tkinterdnd2 import TkinterDnD, DND_FILES


# ---------------- PDF TEXT ----------------
def extract_text(pdf_path, log):
    text = ""

    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except:
                messagebox.showerror("Error", "Cannot decrypt PDF")
                return None

        log.insert(tk.END, f"\n📄 Pages: {len(reader.pages)}\n")

        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()

            log.insert(tk.END, f"Processing page {i+1}\n")
            log.see(tk.END)

            if page_text:
                text += page_text + " "

    return text.strip()


# ---------------- TTS ----------------
async def generate_audio(text, output_file, speed):
    voice = "en-US-AriaNeural"

    communicate = edge_tts.Communicate(
        text,
        voice,
        rate=f"+{speed-100}%"
    )

    await communicate.save(output_file)


def run_tts(text, output_file, speed):
    asyncio.run(generate_audio(text, output_file, speed))


# ---------------- APP ----------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("🎧 PDF → Audiobook (10/10 FIXED)")
        self.root.geometry("600x500")

        self.file_path = None

        # UI
        self.label = tk.Label(root, text="📂 Drag & Drop PDF Here or Select", font=("Arial", 14))
        self.label.pack(pady=10)

        self.log = tk.Text(root, height=18)
        self.log.pack(fill="both", expand=True)

        self.btn_select = tk.Button(root, text="📂 Select PDF", command=self.select_file)
        self.btn_select.pack(pady=5)

        self.btn_convert = tk.Button(root, text="🎙 Convert to MP3", command=self.convert)
        self.btn_convert.pack(pady=5)

        # ---------------- DRAG & DROP FIX ----------------
        root.drop_target_register(DND_FILES)
        root.dnd_bind('<<Drop>>', self.drop_file)

    # ---------------- FILE PICKER ----------------
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])

        if self.file_path:
            self.label.config(text=os.path.basename(self.file_path))

    # ---------------- DRAG DROP ----------------
    def drop_file(self, event):
        file_path = event.data

        # clean curly braces (Mac/Windows fix)
        file_path = file_path.strip("{}")

        if file_path.endswith(".pdf"):
            self.file_path = file_path
            self.label.config(text=os.path.basename(file_path))
            self.log.insert(tk.END, f"\n📥 Loaded: {file_path}\n")
        else:
            messagebox.showerror("Error", "Only PDF files allowed")

    # ---------------- CONVERT ----------------
    def convert(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected")
            return

        self.log.insert(tk.END, "\n🔍 Extracting text...\n")

        text = extract_text(self.file_path, self.log)

        if not text:
            messagebox.showerror("Error", "No text found")
            return

        output_file = os.path.splitext(self.file_path)[0] + ".mp3"

        self.log.insert(tk.END, "\n🎙 Generating audio...\n")

        run_tts(text, output_file, 100)

        self.log.insert(tk.END, f"\n✅ Done: {output_file}\n")
        messagebox.showinfo("Success", "Audio created successfully!")


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = App(root)
    root.mainloop()