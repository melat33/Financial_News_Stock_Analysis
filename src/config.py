# src/config.py - Unified configuration for all tasks
import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Stock tickers to analyze
TICKERS = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'NVDA']

# Data directories
DATA_DIR = PROJECT_ROOT / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
PRICES_DIR = DATA_DIR / 'price'
TECHNICAL_DIR = DATA_DIR / 'technical'
SENTIMENT_DIR = PROCESSED_DATA_DIR / 'sentiment'

# Reports and outputs
REPORTS_DIR = PROJECT_ROOT / 'reports'
PLOTS_DIR = REPORTS_DIR / 'plots'

# File paths
NEWS_FILE = RAW_DATA_DIR / 'financial_news.csv'

# Technical analysis settings
TECHNICAL_INDICATORS = ['SMA', 'EMA', 'RSI', 'MACD', 'BB', 'Stoch']

# Sentiment analysis settings
SENTIMENT_CONFIG = {
    'positive_threshold': 0.1,
    'negative_threshold': -0.1,
    'methods': ['textblob', 'vader', 'combined']
}

# Create directories if they don't exist
directories = [RAW_DATA_DIR, PROCESSED_DATA_DIR, PRICES_DIR, TECHNICAL_DIR, 
               SENTIMENT_DIR, REPORTS_DIR, PLOTS_DIR]

for directory in directories:
    directory.mkdir(parents=True, exist_ok=True)

print("✅ Configuration loaded successfully!")