#!/usr/bin/env python3
import os
import sys
import pandas as pd

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

from src.config import TICKERS, TECHNICAL_DIR
from src.data_loader import DataLoader

def calculate_simple_indicators(price_data):
    """Calculate basic technical indicators without external dependencies"""
    print("🔧 Calculating technical indicators...")
    
    results = []
    
    for ticker in price_data['Stock'].unique():
        stock_data = price_data[price_data['Stock'] == ticker].copy()
        stock_data = stock_data.sort_values('Date')
        
        # Simple Moving Averages
        stock_data['MA_20'] = stock_data['Close'].rolling(window=20).mean()
        stock_data['MA_50'] = stock_data['Close'].rolling(window=50).mean()
        
        # RSI (simplified)
        delta = stock_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        stock_data['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD (simplified)
        exp1 = stock_data['Close'].ewm(span=12).mean()
        exp2 = stock_data['Close'].ewm(span=26).mean()
        stock_data['MACD'] = exp1 - exp2
        stock_data['MACD_Signal'] = stock_data['MACD'].ewm(span=9).mean()
        stock_data['MACD_Histogram'] = stock_data['MACD'] - stock_data['MACD_Signal']
        
        # Bollinger Bands
        stock_data['BB_Middle'] = stock_data['Close'].rolling(window=20).mean()
        bb_std = stock_data['Close'].rolling(window=20).std()
        stock_data['BB_Upper'] = stock_data['BB_Middle'] + (bb_std * 2)
        stock_data['BB_Lower'] = stock_data['BB_Middle'] - (bb_std * 2)
        
        results.append(stock_data)
    
    return pd.concat(results, ignore_index=True)

def run_technical_analysis():
    print("🚀 Starting technical analysis...")
    
    # Load data
    data_loader = DataLoader()
    price_data_dict = data_loader.load_all_price_data()
    
    # Convert dict to DataFrame
    all_data = []
    for ticker, df in price_data_dict.items():
        if not df.empty:
            df['Stock'] = ticker
            all_data.append(df)
    
    if not all_data:
        print("❌ No data found! Run download_data.py first.")
        return
    
    price_data = pd.concat(all_data, ignore_index=True)
    print(f"✅ Loaded data for {len(price_data['Stock'].unique())} stocks")
    
    # Calculate indicators
    technical_data = calculate_simple_indicators(price_data)
    
    # Ensure directory exists
    os.makedirs(TECHNICAL_DIR, exist_ok=True)
    
    # Save results
    technical_file = os.path.join(TECHNICAL_DIR, "technical_indicators.csv")
    technical_data.to_csv(technical_file, index=False)
    
    print(f"✅ Done! Saved {len(technical_data)} records to {technical_file}")
    print(f"📊 Columns: {list(technical_data.columns)}")

if __name__ == "__main__":
    run_technical_analysis()