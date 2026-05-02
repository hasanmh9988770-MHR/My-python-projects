def analyze_text(text):
    if not text:
        return "neutral"

    text = text.lower()

    positive = ["love", "success", "happy", "win", "great", "best"]
    negative = ["sad", "hate", "loss", "bad", "pain"]

    if any(w in text for w in positive):
        return "positive"
    elif any(w in text for w in negative):
        return "negative"
    else:
        return "neutral"