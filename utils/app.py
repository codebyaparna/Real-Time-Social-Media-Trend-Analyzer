import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="SocialPulse AI",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# -----------------------------
# Load Dataset
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Tweets.csv"

df = pd.read_csv(DATA_PATH)
df = df.dropna()

# -----------------------------
# Title
# -----------------------------
st.title("📊 SocialPulse AI")
st.subheader("Real-Time Social Media Trend Analyzer")

st.markdown("---")

# -----------------------------
# KPI Cards
# -----------------------------
total = len(df)
positive = (df["sentiment"] == "positive").sum()
negative = (df["sentiment"] == "negative").sum()
neutral = (df["sentiment"] == "neutral").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tweets", total)
col2.metric("Positive 😊", positive)
col3.metric("Negative 😔", negative)
col4.metric("Neutral 😐", neutral)

st.markdown("---")

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("Dataset Preview")

st.dataframe(df.head(10), use_container_width=True)
# -----------------------------
# Sentiment Charts
# -----------------------------
st.subheader("📈 Sentiment Analysis")

sentiment_count = df["sentiment"].value_counts().reset_index()
sentiment_count.columns = ["Sentiment", "Count"]

col1, col2 = st.columns(2)

with col1:
    pie = px.pie(
        sentiment_count,
        names="Sentiment",
        values="Count",
        title="Sentiment Distribution",
        hole=0.4
    )
    st.plotly_chart(pie, use_container_width=True)

with col2:
    bar = px.bar(
        sentiment_count,
        x="Sentiment",
        y="Count",
        title="Tweets by Sentiment",
        text_auto=True
    )
    st.plotly_chart(bar, use_container_width=True)

st.markdown("---")

# -----------------------------
# Sentiment Filter
# -----------------------------
st.subheader("🔍 Filter Tweets")

option = st.selectbox(
    "Choose Sentiment",
    ["All", "Positive", "Negative", "Neutral"]
)

if option == "All":
    filtered_df = df
else:
    filtered_df = df[df["sentiment"] == option.lower()]

st.write(f"Showing **{len(filtered_df)}** tweets")

st.dataframe(
    filtered_df[["text", "sentiment"]],
    use_container_width=True
)
# -----------------------------
# Word Cloud
# -----------------------------
st.markdown("---")
st.subheader("☁️ Word Cloud")

all_text = " ".join(df["text"].astype(str))

wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color="white",
    colormap="viridis"
).generate(all_text)

fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")

st.pyplot(fig)

# -----------------------------
# Top Trending Words
# -----------------------------
st.markdown("---")
st.subheader("🔥 Top 20 Trending Words")

from collections import Counter
import re

clean_text = re.sub(r"[^a-zA-Z ]", "", all_text.lower())
words = clean_text.split()

stop_words = {
    "the","and","for","that","this","with","have","just","your",
    "from","they","them","then","were","been","will","would",
    "could","should","what","when","where","which","there",
    "about","into","dont","cant","you","are","our","out","too",
    "very","has","had","his","her","she","him","its","it's",
    "was","is","am","not","but","get","got","all"
}

words = [w for w in words if len(w) > 3 and w not in stop_words]

top_words = Counter(words).most_common(20)

trend_df = pd.DataFrame(top_words, columns=["Word", "Count"])

fig = px.bar(
    trend_df,
    x="Word",
    y="Count",
    text_auto=True,
    title="Top Trending Words"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Search Tweets
# -----------------------------
st.markdown("---")
st.subheader("🔎 Search Tweets")

keyword = st.text_input("Enter a keyword")

if keyword:
    result = df[df["text"].str.contains(keyword, case=False, na=False)]

    st.success(f"{len(result)} tweets found")

    st.dataframe(
        result[["text", "sentiment"]],
        use_container_width=True
    )
    # -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📊 SocialPulse AI")
st.sidebar.markdown("---")

st.sidebar.write("### Dataset Statistics")
st.sidebar.write(f"📌 Total Tweets : {total}")
st.sidebar.write(f"😊 Positive : {positive}")
st.sidebar.write(f"😔 Negative : {negative}")
st.sidebar.write(f"😐 Neutral : {neutral}")

st.sidebar.markdown("---")

# Sentiment Percentage
positive_per = round((positive / total) * 100, 2)
negative_per = round((negative / total) * 100, 2)
neutral_per = round((neutral / total) * 100, 2)

st.sidebar.write("### Sentiment Percentage")
st.sidebar.progress(positive_per / 100)
st.sidebar.write(f"Positive : {positive_per}%")

st.sidebar.progress(negative_per / 100)
st.sidebar.write(f"Negative : {negative_per}%")

st.sidebar.progress(neutral_per / 100)
st.sidebar.write(f"Neutral : {neutral_per}%")

st.sidebar.markdown("---")

# Download Dataset
csv = df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="📥 Download Dataset",
    data=csv,
    file_name="Tweets.csv",
    mime="text/csv"
)

# -----------------------------
# Random Tweet
# -----------------------------
st.markdown("---")
st.subheader("🎲 Random Tweet")

if st.button("Generate Random Tweet"):
    tweet = df.sample(1).iloc[0]

    st.info(tweet["text"])
    st.success(f"Sentiment : {tweet['sentiment']}")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.markdown(
    """
    <div style='text-align:center'>
        <h4>📊 SocialPulse AI</h4>
        <p>Real-Time Social Media Trend Analyzer using Python, Pandas, Plotly & Streamlit</p>
        <p>Made with ❤️ by Aparna Singh</p>
    </div>
    """,
    unsafe_allow_html=True
)