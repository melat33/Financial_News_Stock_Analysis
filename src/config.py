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

# ========== TASK 2 CONFIG (Technical Analysis) ==========
TECHNICAL_DIR = os.path.join(DATA_DIR, "technical")
TECHNICAL_INDICATORS = ['SMA', 'EMA', 'RSI', 'MACD', 'BB']
SMA_WINDOWS = [20, 50]
EMA_WINDOWS = [12, 26]
RSI_WINDOW = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_WINDOW = 20
BB_STD = 2

# ========== TASK 3 CONFIG (Sentiment & Correlation) ==========
SENTIMENT_DIR = os.path.join(DATA_DIR, "sentiment")
CORRELATION_DIR = os.path.join(DATA_DIR, "correlation")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Sentiment analysis parameters
SENTIMENT_THRESHOLDS = {
    'positive': 0.1,
    'negative': -0.1,
    'neutral': 0.0
}

# Correlation analysis
CORRELATION_METHODS = ['pearson', 'spearman']
MIN_CORRELATION_SAMPLES = 5

# Create directories
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PRICES_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(TECHNICAL_DIR, exist_ok=True)        # Task 2
os.makedirs(SENTIMENT_DIR, exist_ok=True)        # Task 3  
os.makedirs(CORRELATION_DIR, exist_ok=True)      # Task 3
os.makedirs(REPORTS_DIR, exist_ok=True)          # Task 3

print("✅ Configuration loaded")
print(f"📊 Analyzing 6 companies: {TICKERS}")
print(f"📈 Technical analysis directory: {TECHNICAL_DIR}")
print(f"😊 Sentiment analysis directory: {SENTIMENT_DIR}")