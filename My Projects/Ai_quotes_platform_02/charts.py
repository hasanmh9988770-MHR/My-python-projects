from db import get_all_quotes
from collections import Counter
import datetime

def get_stats():
    quotes = get_all_quotes()

    total = len(quotes)

    authors = Counter([q["author"] for q in quotes if q["author"]])
    top_authors = authors.most_common(5)

    today = datetime.date.today().isoformat()
    today_quotes = [q for q in quotes if q["date"] == today]

    return {
        "total_quotes": total,
        "today_quotes": len(today_quotes),
        "top_authors": top_authors
    }