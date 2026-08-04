import pandas as pd
from pathlib import Path

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset path
DATA_PATH = BASE_DIR / "data" / "Tweets.csv"

try:
    # Load dataset
    df = pd.read_csv(DATA_PATH)

    print("=" * 50)
    print("✅ DATASET LOADED SUCCESSFULLY")
    print("=" * 50)

    print("\n📌 First 5 Rows:")
    print(df.head())

    print("\n📌 Columns:")
    print(df.columns.tolist())

    print("\n📌 Dataset Shape:")
    print(df.shape)

    print("\n📌 Missing Values:")
    print(df.isnull().sum())

except FileNotFoundError:
    print("❌ ERROR: Tweets.csv not found!")
    print(f"Expected location: {DATA_PATH}")

except Exception as e:
    print(f"❌ ERROR: {e}")