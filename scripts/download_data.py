#!/usr/bin/env python3
"""
WINNING DATA DOWNLOAD SCRIPT
Downloads stock price data for technical analysis
"""
import os
import sys
import pandas as pd
import yfinance as yf
from datetime import datetime

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.config import TICKERS

# ✅ CHANGED DIRECTORY: Save data in ../data/price/
DATA_DIR = os.path.join(project_root, 'data')
PRICES_DIR = os.path.join(DATA_DIR, 'price')  # Changed from 'prices' to 'price'
os.makedirs(PRICES_DIR, exist_ok=True)

def download_all_stock_data():
    """Download stock data for all tickers"""
    print("🚀 DOWNLOADING STOCK PRICE DATA")
    print("=" * 60)
    print(f"📊 Tickers: {TICKERS}")
    print(f"📁 Output directory: {PRICES_DIR}")
    print("=" * 60)
    
    success_count = 0
    
    for ticker in TICKERS:
        print(f"\n📥 Downloading {ticker}...")
        
        try:
            # Download data using yfinance
            stock = yf.Ticker(ticker)
            df = stock.history(period="2y")  # 2 years of data
            
            if df.empty:
                print(f"❌ No data available for {ticker}")
                continue
            
            # Reset index and format
            df = df.reset_index()
            df['Date'] = pd.to_datetime(df['Date'])
            df['Stock'] = ticker
            
            # Ensure required columns
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in required_cols:
                if col not in df.columns:
                    print(f"❌ Missing column {col} for {ticker}")
                    continue
            
            # ✅ CHANGED: Save to ../data/price/
            filepath = os.path.join(PRICES_DIR, f"{ticker}.csv")
            df.to_csv(filepath, index=False)
            
            print(f"✅ Downloaded {len(df)} records → {filepath}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error downloading {ticker}: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 DOWNLOAD SUMMARY")
    print('='*60)
    print(f"✅ Successfully downloaded: {success_count}/{len(TICKERS)}")
    print(f"💾 Data saved to: {PRICES_DIR}")
    
    if success_count > 0:
        print("\n🎉 Data download complete! Run technical analysis:")
        print("   python scripts/run_technical.py")
    else:
        print("\n❌ No data downloaded. Check internet connection and try again.")

if __name__ == "__main__":
    # Install yfinance if not available
    try:
        import yfinance
    except ImportError:
        print("📦 Installing yfinance...")
        os.system("pip install yfinance --quiet")
        print("✅ yfinance installed")
    
    # Download all data
    download_all_stock_data()