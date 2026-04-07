from flask import Flask, jsonify, render_template_string
import threading
import time
import requests
import certifi
from collections import Counter

from db import init_db, insert_quote, get_quotes
from ai_model import analyze_text

app = Flask(__name__)

APIS = [
    "https://dummyjson.com/quotes/random",
    "https://zenquotes.io/api/random"
]

# -------------------------
# REAL-TIME BACKGROUND ENGINE
# -------------------------
def fetch_quote():
    for api in APIS:
        try:
            res = requests.get(api, timeout=10, verify=certifi.where())
            data = res.json()

            if "quote" in data:
                return data["quote"], data.get("author", "Unknown")

            if isinstance(data, list):
                return data[0]["q"], data[0]["a"]

        except:
            continue

    return "Keep going.", "AI"


def background_worker():
    init_db()

    while True:
        quote, author = fetch_quote()
        ai = analyze_text(quote)

        insert_quote(
            quote,
            author,
            ai["sentiment"],
            ai["confidence"]
        )

        print("🔥 New quote added:", quote[:40])

        time.sleep(5)  # real-time speed (5 sec)


# -------------------------
# UI
# -------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>REAL-TIME AI DASHBOARD</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        body { background:#0f172a; color:white; font-family:Arial; text-align:center; }
        .card { margin:20px; padding:20px; background:rgba(255,255,255,0.05); border-radius:15px; }
        .quote { border-bottom:1px solid #333; padding:10px; }
    </style>
</head>

<body>

<h1>⚡ REAL-TIME AI QUOTES</h1>

<div class="card">
    <canvas id="chart"></canvas>
</div>

<div class="card">
    <h2>📜 Live Feed</h2>
    <div id="quotes"></div>
</div>

<script>
let chart;

async function loadQuotes(){
    let res = await fetch('/api/quotes');
    let data = await res.json();

    let box = document.getElementById("quotes");
    box.innerHTML = "";

    data.forEach(q=>{
        box.innerHTML += `
        <div class="quote">
            <p>${q.text}</p>
            <b>${q.author}</b> | ${q.sentiment}
        </div>`;
    });
}

async function loadStats(){
    let res = await fetch('/api/stats');
    let data = await res.json();

    if(!chart){
        chart = new Chart(document.getElementById("chart"), {
            type:'doughnut',
            data:{
                labels:Object.keys(data),
                datasets:[{ data:Object.values(data) }]
            }
        });
    } else {
        chart.data.labels = Object.keys(data);
        chart.data.datasets[0].data = Object.values(data);
        chart.update();
    }
}

// REAL-TIME LOOP
setInterval(()=>{
    loadQuotes();
    loadStats();
}, 2000);

loadQuotes();
loadStats();

</script>

</body>
</html>
"""


# -------------------------
# ROUTES
# -------------------------
@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/api/quotes")
def quotes():
    data = get_quotes(30)

    return jsonify([
        {"text": q[1], "author": q[2], "sentiment": q[3]}
        for q in data
    ])


@app.route("/api/stats")
def stats():
    data = get_quotes(100)
    sentiments = [q[3] for q in data]
    return jsonify(dict(Counter(sentiments)))


# -------------------------
# START EVERYTHING
# -------------------------
if __name__ == "__main__":

    # start background worker thread
    thread = threading.Thread(target=background_worker, daemon=True)
    thread.start()

    # start flask
    app.run(debug=True, port=5000)

### To run this in terminal: python app.py
### CREATED BY THE GOAT MHR ###PYTHON 3.14 VERSION USED