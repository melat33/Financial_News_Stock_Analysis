# 📁 src/data_loader.py
import pandas as pd
import os
import sys
import numpy as np
import logging

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.config import NEWS_FILE, PRICES_DIR, DATA_DIR, RAW_DIR, PROCESSED_DIR, TICKERS

def load_news_data():
    """Load news data for EDA analysis with robust datetime parsing"""
    try:
        if not os.path.exists(NEWS_FILE):
            print(f"❌ News file not found: {NEWS_FILE}")
            print("💡 Run: python scripts/download_data.py first")
            return None
            
        # Load with flexible datetime parsing
        df = pd.read_csv(NEWS_FILE)
        
        # Robust datetime parsing - handle multiple formats
        try:
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S%z')
        except:
            try:
                df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
            except:
                try:
                    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
                except:
                    df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Remove any rows with invalid dates
        original_count = len(df)
        df = df.dropna(subset=['date'])
        if len(df) < original_count:
            print(f"⚠️  Removed {original_count - len(df)} rows with invalid dates")
        
        print(f"✅ News data loaded: {len(df)} articles")
        print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"🏢 Companies: {df['stock'].nunique()} companies")
        print(f"📰 Publishers: {df['publisher'].nunique() if 'publisher' in df.columns else 'N/A'}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading news: {e}")
        return None

def validate_news_data(df):
    """Validate and clean news data"""
    print("\n🔍 Validating data quality...")
    
    # Check required columns
    required_cols = ['date', 'headline', 'stock']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"❌ Missing columns: {missing_cols}")
        return None
    
    # Basic stats
    print(f"📊 Total articles: {len(df):,}")
    print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"🏢 Companies covered: {sorted(df['stock'].unique())}")
    
    # Text statistics
    df['headline_length'] = df['headline'].str.len()
    df['word_count'] = df['headline'].str.split().str.len()
    
    print(f"🔤 Headline stats:")
    print(f"   - Average length: {df['headline_length'].mean():.1f} chars")
    print(f"   - Average words: {df['word_count'].mean():.1f}")
    
    if 'publisher' in df.columns:
        print(f"📰 Publishers: {df['publisher'].nunique()}")
        print(f"🏆 Top publishers:")
        print(df['publisher'].value_counts().head(5))
    
    return df

def load_stock_data(ticker="all"):
    """Load stock price data that works with multi-company data from Task 1 & 2"""
    try:
        print(f"📊 Loading stock data for: {ticker}")
        
        # Try to load the combined stock data that should already exist from Task 1/2
        possible_paths = [
            os.path.join(PRICES_DIR, "all_stocks.csv"),
            os.path.join(PROCESSED_DIR, "stock_data_combined.csv"),
            os.path.join(DATA_DIR, "combined_stocks.csv"),
            os.path.join(PRICES_DIR, "AAPL.csv")  # Fallback to single company
        ]
        
        stock_df = None
        used_path = None
        
        for path in possible_paths:
            if os.path.exists(path):
                stock_df = pd.read_csv(path)
                used_path = path
                print(f"✅ Found stock data at: {path}")
                print(f"📋 Columns: {list(stock_df.columns)}")
                break
        
        if stock_df is None:
            print("❌ No combined stock data found")
            print("💡 Creating sample multi-company data for demonstration...")
            return create_sample_multi_company_data()
            
        # Handle different column names for multi-company data
        date_columns = ['date', 'Date', 'DATE', 'timestamp', 'Time', 'datetime']
        date_col = None
        for col in date_columns:
            if col in stock_df.columns:
                date_col = col
                break
        
        if date_col:
            stock_df['date'] = pd.to_datetime(stock_df[date_col])
            print(f"✅ Using date column: '{date_col}'")
        else:
            print("❌ No date column found")
            return None
        
        # Handle ticker/company column
        ticker_columns = ['ticker', 'Ticker', 'TICKER', 'stock', 'Stock', 'STOCK', 'symbol', 'Symbol']
        ticker_col = None
        for col in ticker_columns:
            if col in stock_df.columns:
                ticker_col = col
                break
        
        if ticker_col:
            stock_df['ticker'] = stock_df[ticker_col]
            print(f"✅ Using ticker column: '{ticker_col}'")
        else:
            # If no ticker column, assume it's single company data
            print("⚠️  No ticker column found - assuming single company data")
            stock_df['ticker'] = 'AAPL'  # Default ticker
        
        # Handle close price column
        close_columns = ['close', 'Close', 'CLOSE', 'price', 'Price', 'Adj Close', 'adj_close']
        close_col = None
        for col in close_columns:
            if col in stock_df.columns:
                close_col = col
                break
        
        if close_col:
            stock_df['close'] = pd.to_numeric(stock_df[close_col], errors='coerce')
            print(f"✅ Using close column: '{close_col}'")
        else:
            print("❌ No close price column found")
            return None
        
        # Filter for specific ticker if requested
        if ticker != "all" and 'ticker' in stock_df.columns:
            original_count = len(stock_df)
            stock_df = stock_df[stock_df['ticker'] == ticker].copy()
            print(f"✅ Filtered for {ticker}: {len(stock_df)} records (from {original_count} total)")
        
        # Sort by date and ticker
        stock_df = stock_df.sort_values(['date', 'ticker'])
        
        print(f"✅ Final stock data: {len(stock_df)} records")
        print(f"📅 Date range: {stock_df['date'].min()} to {stock_df['date'].max()}")
        if 'ticker' in stock_df.columns:
            print(f"🏢 Companies: {stock_df['ticker'].nunique()} companies")
            print(f"📈 Tickers: {sorted(stock_df['ticker'].unique())}")
        
        return stock_df[['date', 'close', 'ticker']].copy()
        
    except Exception as e:
        print(f"❌ Error loading stock data: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_sample_multi_company_data():
    """Create sample multi-company data that matches Task 1/2 structure"""
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    all_stocks = []
    
    for ticker in TICKERS:
        base_price = 100 + (TICKERS.index(ticker) * 20)  # Different base prices
        stock_data = pd.DataFrame({
            'date': dates,
            'close': [base_price + i * 0.5 + np.random.normal(0, 2) for i in range(100)],
            'volume': [1000000 + i * 10000 for i in range(100)],
            'ticker': ticker
        })
        all_stocks.append(stock_data)
    
    combined_df = pd.concat(all_stocks, ignore_index=True)
    print("✅ Created sample multi-company stock data")
    print(f"🏢 Companies: {TICKERS}")
    print(f"📊 Total records: {len(combined_df)}")
    
    return combined_df[['date', 'close', 'ticker']]

def load_all_stocks_data(tickers=None):
    """Load stock data for multiple tickers"""
    if tickers is None:
        tickers = TICKERS
    
    all_stocks = []
    for ticker in tickers:
        stock_data = load_stock_data(ticker)
        if stock_data is not None:
            stock_data['ticker'] = ticker
            all_stocks.append(stock_data)
    
    if all_stocks:
        combined_df = pd.concat(all_stocks, ignore_index=True)
        print(f"✅ Loaded stock data for {len(tickers)} tickers")
        return combined_df
    else:
        print("❌ No stock data loaded")
        return None

class DataLoader:
    """
    DataLoader class for backward compatibility with notebooks
    This wraps the existing functional approach in a class structure
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_news_data(self):
        """Load news data using the existing function"""
        return load_news_data()
    
    def validate_news_data(self, df):
        """Validate news data using the existing function"""
        return validate_news_data(df)
    
    def load_stock_data(self, ticker="all"):
        """Load stock data using the existing function"""
        return load_stock_data(ticker)
    
    def load_all_stocks_data(self, tickers=None):
        """Load all stocks data using the existing function"""
        return load_all_stocks_data(tickers)
    
    def get_available_tickers(self):
        """Get list of available tickers"""
        return TICKERS

# Create singleton instance for easy import
data_loader = DataLoader()