import tkinter as tk
from tkinter import messagebox
import random
import time
from itertools import product

# ===================== GAME STATE ===================== #
class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.turn = 0
        self.guess = []
        self.running = True
        self.start_time = time.time()


# ===================== RULE ENGINE ===================== #
class RulesEngine:
    def __init__(self, colors):
        self.colors = colors
        self.secret = []

    def new_round(self):
        self.secret = random.sample(self.colors, 4)

    def evaluate(self, guess):
        s = self.secret[:]
        g = list(guess)
        red = gray = 0

        for i in range(3, -1, -1):
            if g[i] == s[i]:
                red += 1
                g.pop(i)
                s.pop(i)

        for c in g:
            if c in s:
                gray += 1
                s.remove(c)

        return red, gray


# ===================== AI ENGINE (STABLE MODE) ===================== #
class AAAAI:
    def __init__(self, colors):
        self.colors = colors
        self.reset()

    def reset(self):
        self.candidates = list(product(self.colors, repeat=4))
        random.shuffle(self.candidates)

    def evaluate_like_game(self, secret, guess):
        s = secret[:]
        g = list(guess)
        red = gray = 0

        for i in range(len(g)-1, -1, -1):
            if g[i] == s[i]:
                red += 1
                g.pop(i)
                s.pop(i)

        for c in g:
            if c in s:
                gray += 1
                s.remove(c)

        return red, gray

    def update(self, guess, red, gray):
        self.candidates = [
            c for c in self.candidates
            if self.evaluate_like_game(list(c), guess) == (red, gray)
        ]

    def next_move(self):
        if not self.candidates:
            self.reset()
        return list(self.candidates[0])


# ===================== ENGINE CORE ===================== #
class AAAEngine:
    def __init__(self, root):
        self.root = root
        self.root.title("🔥 AAA ENGINE GOD MODE v2")
        self.root.geometry("560x900")
        self.root.configure(bg="#0a0a0a")

        self.colors = [
            "#270101", "#F08B33", "#776B04", "#F1B848",
            "#8F715B", "#0486DB", "#C1403D", "#F3D4A0"
        ]

        self.state = GameState()
        self.rules = RulesEngine(self.colors)
        self.ai = AAAAI(self.colors)

        self.scene = "menu"
        self.cells = {}

        self.build_ui()
        self.timer_loop()

    # ================= UI ================= #
    def build_ui(self):
        tk.Label(
            self.root, text="🔥 AAA ENGINE GOD MODE v2",
            fg="white", bg="#0a0a0a",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        self.info = tk.Label(
            self.root, text="Scene: MENU",
            fg="gray", bg="#0a0a0a"
        )
        self.info.pack()

        self.timer = tk.Label(
            self.root, text="⏱ 0s",
            fg="lime", bg="#0a0a0a"
        )
        self.timer.pack()

        # BOARD
        board = tk.Frame(self.root, bg="#0a0a0a")
        board.pack(pady=15)

        for r in range(10):
            for c in range(4):
                cell = tk.Label(
                    board, width=6, height=3,
                    bg="#222", relief="raised"
                )
                cell.grid(row=r, column=c, padx=3, pady=3)
                self.cells[(r, c)] = cell

        # PALETTE
        palette = tk.Frame(self.root, bg="#0a0a0a")
        palette.pack(pady=10)

        for col in self.colors:
            btn = tk.Label(
                palette, bg=col, width=4, height=2,
                relief="raised", cursor="hand2"
            )
            btn.pack(side="left", padx=3)
            btn.bind("<Button-1>", lambda e, c=col: self.pick(c))

        # CONTROLS
        self.btn("🚀 START", self.start_game).pack(pady=5)
        self.btn("🤖 AI MODE", self.ai_mode).pack(pady=5)
        self.btn("🔁 RESET", self.reset_all).pack(pady=5)

    def btn(self, text, cmd):
        b = tk.Label(
            self.root, text=text,
            fg="black", bg="white",
            width=22, height=2,
            font=("Arial", 12, "bold"),
            cursor="hand2"
        )
        b.bind("<Button-1>", lambda e: cmd())
        return b

    # ================= GAMEPLAY ================= #
    def start_game(self):
        self.scene = "game"
        self.rules.new_round()
        self.state.reset()
        self.clear_board()
        self.info.config(text="Scene: GAME")

    def pick(self, color):
        if self.scene != "game":
            return

        if len(self.state.guess) < 4:
            idx = len(self.state.guess)
            self.cells[(self.state.turn, idx)].config(bg=color)
            self.state.guess.append(color)

        if len(self.state.guess) == 4:
            self.root.after(200, self.resolve)

    def resolve(self):
        red, gray = self.rules.evaluate(self.state.guess)

        if red == 4:
            self.win(False)
            return

        self.state.turn += 1
        self.state.guess = []

        if self.state.turn >= 10:
            self.lose()

    # ================= AI MODE ================= #
    def ai_mode(self):
        self.start_game()
        self.scene = "ai"
        self.ai.reset()
        self.info.config(text="Scene: AI MODE")
        self.root.after(500, self.ai_step)

    def ai_step(self):
        if self.scene != "ai":
            return

        guess = self.ai.next_move()

        for i in range(4):
            self.cells[(self.state.turn, i)].config(bg=guess[i])

        red, gray = self.rules.evaluate(guess)

        if red == 4:
            self.win(True)
            return

        self.ai.update(guess, red, gray)
        self.state.turn += 1

        if self.state.turn >= 10:
            self.lose()
            return

        self.root.after(500, self.ai_step)

    # ================= END STATES ================= #
    def win(self, ai):
        self.scene = "menu"
        msg = "🤖 AI WINS" if ai else "🏆 PLAYER WINS"
        messagebox.showinfo("GAME END", msg)
        self.reset_all()

    def lose(self):
        self.scene = "menu"
        messagebox.showwarning("GAME OVER", "💀 Machine Dominated You")
        self.reset_all()

    def reset_all(self):
        self.scene = "menu"
        self.state.reset()
        self.ai.reset()
        self.clear_board()
        self.info.config(text="Scene: MENU")

    def clear_board(self):
        for c in self.cells.values():
            c.config(bg="#222")

    # ================= TIMER ================= #
    def timer_loop(self):
        if self.scene in ["game", "ai"]:
            self.timer.config(
                text=f"⏱ {int(time.time() - self.state.start_time)}s"
            )

        self.root.after(1000, self.timer_loop)


# ================= RUN ================= #
if __name__ == "__main__":
    root = tk.Tk()
    AAAEngine(root)
    root.mainloop()

### Game Summary:
### Guess a hidden 4-color code in 10 tries. After each guess, you get feedback.
### 🔴 red means correct color and position, ⚪ gray means correct color but wrong position.
### You win if you get all 4 reds; otherwise you lose after 10 attempts. In AI mode, the computer uses logic to solve the code automatically.