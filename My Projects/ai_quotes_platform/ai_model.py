from transformers import pipeline

model = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)


def analyze_text(text):
    result = model(text[:512])[0]

    return {
        "sentiment": result["label"],
        "confidence": round(result["score"], 4)
    }