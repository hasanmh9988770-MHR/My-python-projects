import matplotlib
matplotlib.use('Agg')  # ✅ FIX FOR MAC THREAD ERROR

import matplotlib.pyplot as plt
import sqlite3
import pandas as pd


def load_data():
    conn = sqlite3.connect("quotes.db")
    df = pd.read_sql_query("SELECT * FROM quotes", conn)
    conn.close()
    return df


def create_charts():
    df = load_data()

    if df.empty:
        return  # avoid crash if no data

    # Author chart
    author_counts = df["author"].value_counts().head(5)
    plt.figure()
    author_counts.plot(kind="bar")
    plt.title("Top Authors")
    plt.savefig("static/authors.png")
    plt.close()

    # Sentiment chart
    sentiment_counts = df["sentiment"].value_counts()
    plt.figure()
    sentiment_counts.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Sentiment Distribution")
    plt.savefig("static/sentiment.png")
    plt.close()