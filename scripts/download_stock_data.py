# scripts/download_stock_data_fixed.py
import yfinance as yf
import pandas as pd
from pathlib import Path
import sys

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.config import TICKERS, RAW_DIR
from datetime import datetime, timedelta

def download_stock_data():
    """Download missing stock data with robust path handling"""
    print("📥 Downloading stock data...")
    
    # Convert RAW_DIR to Path if it's a string
    if isinstance(RAW_DIR, str):
        raw_dir_path = Path(RAW_DIR)
    else:
        raw_dir_path = RAW_DIR
    
    # Create directory if it doesn't exist
    raw_dir_path.mkdir(parents=True, exist_ok=True)
    
    # Date range (last 2 years for good data coverage)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)  # 2 years
    
    success_count = 0
    for ticker in TICKERS:
        file_path = raw_dir_path / f"{ticker}.csv"
        
        try:
            print(f"📥 Downloading {ticker}...")
            stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            if not stock_data.empty:
                stock_data.reset_index(inplace=True)
                stock_data.to_csv(file_path, index=False)
                print(f"✅ Saved {ticker}: {len(stock_data)} records")
                print(f"   Date range: {stock_data['Date'].min()} to {stock_data['Date'].max()}")
                success_count += 1
            else:
                print(f"❌ No data found for {ticker}")
                
        except Exception as e:
            print(f"❌ Error downloading {ticker}: {e}")
    
    print(f"\n🎉 Downloaded {success_count} out of {len(TICKERS)} stock files")
    return success_count

if __name__ == "__main__":
    download_stock_data()