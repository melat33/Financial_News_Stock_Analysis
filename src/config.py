# 📁 src/config.py
import os

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PRICES_DIR = os.path.join(DATA_DIR, "prices")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# The 6 companies we're analyzing
TICKERS = ["AAPL", "AMZN", "GOOG", "META", "MSFT", "NVDA"]

# News file
NEWS_FILE = os.path.join(RAW_DIR, "raw_analyst_ratings.csv")

# Create directories
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PRICES_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

print("✅ Configuration loaded")
print(f"📊 Analyzing 6 companies: {TICKERS}")