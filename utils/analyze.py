import pandas as pd
from pathlib import Path
from collections import Counter

# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset path
DATA_PATH = BASE_DIR / "data" / "Tweets.csv"

# Load dataset
df = pd.read_csv(DATA_PATH)

# Remove missing values
df = df.dropna()

# Clean text
df["clean_text"] = df["text"].str.lower()
df["clean_text"] = df["clean_text"].str.replace(r"http\S+", "", regex=True)
df["clean_text"] = df["clean_text"].str.replace(r"[^a-zA-Z ]", "", regex=True)

# Get all words
words = " ".join(df["clean_text"]).split()

# Remove short words
words = [word for word in words if len(word) > 3]

# Count top words
top_words = Counter(words).most_common(20)

print("=" * 50)
print("      SOCIAL PULSE AI ANALYSIS")
print("=" * 50)

print("\nTotal Tweets:")
print(len(df))

print("\nSentiment Distribution:")
print(df["sentiment"].value_counts())

print("\nTop 20 Trending Words:")
for word, count in top_words:
    print(f"{word} : {count}")