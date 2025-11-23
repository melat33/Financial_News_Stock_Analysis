# src/config.py - Unified for both Task 1 and Task 2
import os

# Project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Stock tickers to analyze
TICKERS = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'NVDA']

# File paths
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
PRICES_DIR = os.path.join(DATA_DIR, 'price')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')
PLOTS_DIR = os.path.join(REPORTS_DIR, 'plots')

# News data file
NEWS_FILE = os.path.join(RAW_DATA_DIR, 'financial_news.csv')

# Technical analysis settings
TECHNICAL_INDICATORS = ['SMA', 'EMA', 'RSI', 'MACD', 'BB', 'Stoch']

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, PRICES_DIR, REPORTS_DIR, PLOTS_DIR]:
    os.makedirs(directory, exist_ok=True)

print("✅ Configuration loaded successfully!")