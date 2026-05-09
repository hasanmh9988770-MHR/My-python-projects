from transformers import pipeline

# Load model once (faster + clean)
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def chunk_text(text, max_chars=2500):
    """
    Split long text into safe chunks
    """
    text = text.strip()
    chunks = []

    while len(text) > max_chars:
        split_point = text.rfind(".", 0, max_chars)
        if split_point == -1:
            split_point = max_chars

        chunks.append(text[:split_point + 1])
        text = text[split_point + 1:]

    chunks.append(text)
    return chunks


def summarize_text(text):
    """
    Main summarization function
    """
    text = text.strip()

    if len(text) < 50:
        return "Text too short to summarize."

    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks:
        result = summarizer(
            chunk,
            max_length=80,
            min_length=25,
            do_sample=False
        )
        summaries.append(result[0]["summary_text"])

    return " ".join(summaries)

    ### PYTHON 3.9.6 VERSION USED
    ### TO RUN THIS: streamlit run app.py
    ### CREATED MY THE GOAT MHR