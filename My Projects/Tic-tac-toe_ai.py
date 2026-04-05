import os
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
from flask import Flask, render_template, request, jsonify

# ---------- FIX PATH ISSUE ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates")
)

# ---------- GAME LOGIC ----------

def check_winner(board):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]

    if "" not in board:
        return "Draw"

    return None


# ---------- MINIMAX AI ----------

def minimax(board, is_max):
    result = check_winner(board)

    if result == "O":
        return 1
    if result == "X":
        return -1
    if result == "Draw":
        return 0

    if is_max:
        best = -999
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                best = max(best, minimax(board, False))
                board[i] = ""
        return best
    else:
        best = 999
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                best = min(best, minimax(board, True))
                board[i] = ""
        return best


def best_move(board):
    best_score = -999
    move = None

    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""

            if score > best_score:
                best_score = score
                move = i

    return move


# ---------- ROUTES ----------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    board = data.get("board", [""] * 9)

    ai = best_move(board)
    if ai is not None:
        board[ai] = "O"

    winner = check_winner(board)

    return jsonify({
        "board": board,
        "winner": winner
    })


@app.route("/reset", methods=["POST"])
def reset():
    return jsonify({
        "board": [""] * 9,
        "winner": None
    })

@app.route("/favicon.ico")
def favicon():
    return "", 204


# ---------- RUN SERVER ----------

if __name__ == "__main__":
    import os

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print("\n🔥 SERVER STARTED")
        print("👉 Open: http://127.0.0.1:5001\n")

    app.run(debug=True, port=5001)

### CREATED BY MEHEDI HASAN RABBY~GOAT MHR
### TO RUN THIS IN TERMINAL: python "My Projects/Tic-tac-toe_ai.py"
### PYTHON VERSION 3.14 USED