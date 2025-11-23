# 📁 config.py - UPDATED FOR TASK 2
import os

# Project paths - FIXED: removed one os.path.dirname
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PRICES_DIR = os.path.join(DATA_DIR, "price")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
TECHNICAL_DIR = os.path.join(PROCESSED_DIR, "technical_indicators")

# The 6 companies we're analyzing
TICKERS = ["AAPL", "AMZN", "GOOG", "META", "MSFT", "NVDA"]

# News file
NEWS_FILE = os.path.join(RAW_DIR, "raw_analyst_ratings.csv")

# Technical Analysis Configuration
TECHNICAL_INDICATORS = {
    'moving_averages': [5, 10, 20, 50, 200],
    'rsi_period': 14,
    'macd_fast': 12,
    'macd_slow': 26, 
    'macd_signal': 9,
    'bollinger_period': 20,
    'bollinger_std': 2,
    'stochastic_period': 14,
    'adx_period': 14,
    'atr_period': 14
}

# Trading Strategy Parameters
TRADING_STRATEGY = {
    'rsi_oversold': 30,
    'rsi_overbought': 70,
    'signal_threshold_buy': 0.3,
    'signal_threshold_sell': -0.3,
    'volume_threshold': 1.2  # 20% above average volume
}

# Visualization Settings
CHART_STYLES = {
    'company_colors': {
        'AAPL': '#A2AAAD', 'AMZN': '#FF9900', 'GOOG': '#4285F4',
        'META': '#1877F2', 'MSFT': '#737373', 'NVDA': '#76B900'
    },
    'chart_size': (15, 8),
    'style': 'seaborn-v0_8'
}

# Create directories
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PRICES_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(TECHNICAL_DIR, exist_ok=True)

print("✅ Configuration loaded for Task 2 - Technical Analysis")
print(f"📊 Analyzing {len(TICKERS)} companies: {TICKERS}")
print(f"📈 Technical indicators configured: {len(TECHNICAL_INDICATORS)} parameters")