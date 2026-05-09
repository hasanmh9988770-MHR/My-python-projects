import streamlit as st
from summarizer import summarize_text

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="🧠",
    layout="centered"
)

# =========================
# UI HEADER
# =========================
st.title("🧠 AI Text Summarizer")
st.write("Paste your long text and get a clean AI summary instantly.")

# =========================
# INPUT BOX
# =========================
text_input = st.text_area(
    "Enter your text here:",
    height=300,
    placeholder="Paste your article, story, or paragraph..."
)

# =========================
# BUTTON
# =========================
if st.button("🚀 Summarize"):
    if not text_input.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Generating summary..."):
            result = summarize_text(text_input)

        st.success("Done!")
        st.subheader("📌 Summary")
        st.write(result)