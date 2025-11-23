#!/usr/bin/env python3
import os
import sys
import pandas as pd
import numpy as np

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.config import TICKERS, TECHNICAL_DIR

def calculate_simple_indicators(price_data):
    """Calculate basic technical indicators without external dependencies"""
    print("🔧 Calculating technical indicators...")
    
    results = []
    
    for ticker in price_data['Stock'].unique():
        stock_data = price_data[price_data['Stock'] == ticker].copy()
        stock_data = stock_data.sort_values('Date')
        
        # Simple Moving Averages
        stock_data['MA_20'] = stock_data['Close'].rolling(window=20, min_periods=1).mean()
        stock_data['MA_50'] = stock_data['Close'].rolling(window=50, min_periods=1).mean()
        
        # RSI (simplified)
        delta = stock_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=1).mean()
        rs = gain / loss
        stock_data['RSI'] = 100 - (100 / (1 + rs))
        
        # Handle division by zero in RSI
        stock_data['RSI'] = stock_data['RSI'].fillna(50)
        
        # MACD (simplified)
        exp1 = stock_data['Close'].ewm(span=12, min_periods=1).mean()
        exp2 = stock_data['Close'].ewm(span=26, min_periods=1).mean()
        stock_data['MACD'] = exp1 - exp2
        stock_data['MACD_Signal'] = stock_data['MACD'].ewm(span=9, min_periods=1).mean()
        stock_data['MACD_Histogram'] = stock_data['MACD'] - stock_data['MACD_Signal']
        
        # Bollinger Bands
        stock_data['BB_Middle'] = stock_data['Close'].rolling(window=20, min_periods=1).mean()
        bb_std = stock_data['Close'].rolling(window=20, min_periods=1).std()
        stock_data['BB_Upper'] = stock_data['BB_Middle'] + (bb_std * 2)
        stock_data['BB_Lower'] = stock_data['BB_Middle'] - (bb_std * 2)
        
        # Fill NaN values
        stock_data = stock_data.fillna(method='bfill').fillna(method='ffill')
        
        results.append(stock_data)
        print(f"✅ Calculated indicators for {ticker}")
    
    return pd.concat(results, ignore_index=True)

def load_sample_data():
    """Create sample price data for testing if no real data exists"""
    print("📊 Generating sample price data...")
    
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    all_data = []
    
    for ticker in TICKERS:
        # Create realistic sample data
        np.random.seed(hash(ticker) % 10000)  # Different seed for each ticker
        
        # Start with realistic prices
        base_price = np.random.uniform(50, 500)
        returns = np.random.normal(0.001, 0.02, len(dates))
        prices = base_price * (1 + returns).cumprod()
        
        df = pd.DataFrame({
            'Date': dates,
            'Open': prices * 0.99,  # Slightly lower than close
            'High': prices * 1.02,  # Higher than close
            'Low': prices * 0.98,   # Lower than close
            'Close': prices,
            'Volume': np.random.randint(1000000, 10000000, len(dates)),
            'Stock': ticker
        })
        
        all_data.append(df)
    
    return pd.concat(all_data, ignore_index=True)

def run_technical_analysis():
    print("🚀 Starting technical analysis...")
    
    # Try to load existing price data first
    price_data = None
    price_files = []
    
    # Check for price data files
    for ticker in TICKERS:
        price_file = os.path.join('data', 'price', f'{ticker}_price.csv')
        if os.path.exists(price_file):
            price_files.append(price_file)
    
    if price_files:
        print(f"📁 Found {len(price_files)} price data files")
        all_data = []
        for file in price_files:
            try:
                df = pd.read_csv(file)
                ticker = os.path.basename(file).replace('_price.csv', '')
                df['Stock'] = ticker
                all_data.append(df)
            except Exception as e:
                print(f"❌ Error loading {file}: {e}")
        
        if all_data:
            price_data = pd.concat(all_data, ignore_index=True)
    
    # If no price data found, use sample data
    if price_data is None or price_data.empty:
        print("❌ No existing price data found. Using sample data...")
        price_data = load_sample_data()
        
        # Save sample data for future use
        sample_dir = os.path.join('data', 'price')
        os.makedirs(sample_dir, exist_ok=True)
        for ticker in TICKERS:
            ticker_data = price_data[price_data['Stock'] == ticker]
            ticker_data.to_csv(os.path.join(sample_dir, f'{ticker}_price.csv'), index=False)
        print("💾 Sample price data saved for future use")
    
    print(f"✅ Loaded data for {len(price_data['Stock'].unique())} stocks")
    print(f"📅 Date range: {price_data['Date'].min()} to {price_data['Date'].max()}")
    
    # Calculate indicators
    technical_data = calculate_simple_indicators(price_data)
    
    # Ensure directory exists
    os.makedirs(TECHNICAL_DIR, exist_ok=True)
    
    # Save results
    technical_file = os.path.join(TECHNICAL_DIR, "technical_indicators.csv")
    technical_data.to_csv(technical_file, index=False)
    
    print(f"✅ Done! Saved {len(technical_data)} records to {technical_file}")
    print(f"📊 Columns: {list(technical_data.columns)}")
    
    # Show summary
    for ticker in technical_data['Stock'].unique():
        ticker_data = technical_data[technical_data['Stock'] == ticker]
        print(f"   {ticker}: {len(ticker_data)} records, RSI range: {ticker_data['RSI'].min():.1f}-{ticker_data['RSI'].max():.1f}")

if __name__ == "__main__":
    run_technical_analysis()