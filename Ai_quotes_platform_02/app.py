import threading
import time
import requests
import random
from flask import Flask, render_template, jsonify

# Import your custom modules
from db import init_db, get_all_quotes, insert_quote
from charts import get_stats

app = Flask(__name__)

# --- GLOBAL TRACKER ---
# This stays outside the functions to remember what was last posted
last_generated_text = ""


# --- 1. THE AUTO-BOT LOGIC ---
def run_bot():
    """Background worker that simulates users posting quotes"""
    time.sleep(5)
    print("🚀 AUTO-POSTER BOT IS LIVE!")

    while True:
        try:
            requests.get("http://127.0.0.1:5001/api/generate", timeout=5)
        except Exception as e:
            print(f"🤖 Bot waiting for server...")

        time.sleep(5)


# --- 2. THE WEBSITE ROUTES ---

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/stats")
def stats():
    return jsonify(get_stats())


@app.route("/api/live")
def live():
    quotes = get_all_quotes()
    return jsonify([
        {"text": q["text"], "author": q["author"]} for q in quotes[::-1]
    ])


@app.route("/api/generate")
def generate():
    global last_generated_text

    # Expanded Library to ensure variety
    samples = [
        ("Code is like humor. When you have to explain it, it’s bad.", "Cory House"),
        ("Fix the cause, not the symptom.", "Steve McConnell"),
        ("Stay hungry, stay foolish.", "Steve Jobs"),
        ("Simplicity is the soul of efficiency.", "Austin Freeman"),
        ("Talk is cheap. Show me the code.", "Linus Torvalds"),
        ("Design is how it works.", "Steve Jobs"),
        ("The hard way is the right way.", "Jocko Willink"),
        ("Clean code always looks like it was written by someone who cares.", "Robert C. Martin"),
        ("First, solve the problem. Then, write the code.", "John Johnson"),
        ("Experience is the name everyone gives to their mistakes.", "Oscar Wilde"),
        ("Knowledge is power.", "Francis Bacon"),
        ("Confusion is part of programming.", "Felienne Hermans"),
        ("Don't comment bad code—rewrite it.", "Brian Kernighan"),
        ("A user interface is like a joke. If you have to explain it, it’s not that good.", "Martin LeBlanc"),
        ("The best thing about a boolean is even if you are wrong, you are only off by a bit.", "Anonymous"),
        ("Before software can be reusable it first has to be usable.", "Ralph Johnson"),
        ("Make it work, make it right, make it fast.", "Kent Beck"),
        ("Programming is the art of telling another human what they want the computer to do.", "Donald Knuth"),
        ("In order to be irreplaceable, one must always be different.", "Coco Chanel"),
        ("Computers are good at following instructions, but not at reading your mind.", "Donald Knuth"),
        ("Work hard in silence, let your success be your noise.", "Frank Ocean")
    ]

    # Anti-Repeat Logic: Pick a random quote, but re-roll if it's the same as the last one
    q = random.choice(samples)
    while q[0] == last_generated_text:
        q = random.choice(samples)

    last_generated_text = q[0]

    # Save to Database
    insert_quote(q[0], q[1])

    print(f"✨ Bot posted: {q[0]}")
    return jsonify({"status": "Success", "quote": q[0]})


# --- 3. THE LAUNCHER ---

if __name__ == "__main__":
    init_db()
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print("🔥 Starting QuotesGram on http://127.0.0.1:5001")
    # CHANGE THIS LINE:
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)

### CREATED BY THE GOAT MHR ~ MEHEDI HASAN RABBY
### PYTHON VERSION 3.14 USED
### To run this in terminal: cd "My Projects/Ai_quotes_platform_02"
### python app.py