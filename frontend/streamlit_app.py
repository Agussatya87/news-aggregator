# frontend/streamlit_app.py
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="AI News Aggregator", layout="wide")

st.title("📰 AI News Aggregator")
# st.write("Backend host:", BACKEND)  # bisa di-comment kalau tidak perlu debug

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("Filter")

categories = [
    "All categories",
    "Politics",
    "Economy",
    "Technology",
    "Sports",
    "Health",
    "Entertainment",
    "World",
    "General",
]
selected_category = st.sidebar.selectbox("Filter category", categories, index=0)

limit = st.sidebar.number_input(
    "Number of news",
    min_value=1,
    max_value=100,
    value=20,
    step=1,
)

q = st.sidebar.text_input("Search keyword (optional)")


def fetch_news():
    params = {"limit": int(limit)}

    if selected_category != "All categories":
        params["topic"] = selected_category

    if q:
        params["q"] = q

    try:
        r = requests.get(f"{BACKEND}/news", params=params, timeout=10)
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")
        st.stop()

    if not r.ok:
        st.error("Backend returned error (not 2xx).")
        st.code(r.text[:1000], language="text")
        st.stop()

    try:
        return r.json()
    except Exception as e:
        st.error(f"Failed to decode JSON from backend: {e}")
        st.code(r.text[:1000], language="text")
        st.stop()


data = fetch_news()

st.subheader(f"Total: {data['total']} news")

for item in data["items"]:
    st.markdown("---")
    st.markdown(f"### {item['title']}")

    # 🖼️ Tampilkan gambar kalau ada
    if item.get("image_url"):
        st.image(item["image_url"], width="stretch")

    meta = []
    if item.get("source"):
        meta.append(f"**Sumber:** {item['source']}")
    if item.get("topic"):
        meta.append(f"**Topik:** {item['topic']}")
    if item.get("sentiment"):
        meta.append(f"**Sentimen:** {item['sentiment']}")
    if item.get("published_at"):
        meta.append(f"**Tanggal:** {str(item['published_at'])[:10]}")
    if meta:
        st.markdown(" | ".join(meta))

    if item.get("summary"):
        st.markdown("**Ringkasan AI:**")
        st.write(item["summary"])


    if item.get("url"):
        st.markdown(f"[Baca di sumber asli]({item['url']})")
