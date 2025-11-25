# src/data_loader.py
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path
from .config import *

class DataLoader:
    """Unified data loader for all tasks"""
    
    def __init__(self):
        self.news_data = None
        self.price_data = {}
    
    def load_news_data(self):
        """Load news data for Task 1 - FIXED to always return DataFrame"""
        print("📰 Loading news data...")
        
        try:
            if not NEWS_FILE.exists():
                print(f"❌ News file not found: {NEWS_FILE}")
                print("💡 Please run: python scripts/download_news.py")
                return pd.DataFrame()
            
            df = pd.read_csv(NEWS_FILE)
            
            # Check if required columns exist
            required_cols = ['date', 'headline', 'stock']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                print(f"❌ Missing required columns: {missing_cols}")
                return pd.DataFrame()
            
            # Safe datetime conversion
            df['date'] = self._safe_datetime_conversion(df['date'])
            
            # Filter for target companies
            df = df[df['stock'].isin(TICKERS)]
            
            print(f"✅ Loaded news data: {len(df)} articles")
            print(f"   Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
            print(f"   Companies: {df['stock'].nunique()} companies")
            
            self.news_data = df
            return df
            
        except Exception as e:
            print(f"❌ Error loading news data: {e}")
            return pd.DataFrame()
    
    def _safe_datetime_conversion(self, series):
        """Safely convert series to datetime, handling timezone issues"""
        try:
            # First try without timezone
            result = pd.to_datetime(series, errors='coerce')
            
            # If we have timezone-aware dates, convert to timezone-naive
            if hasattr(result, 'dt') and result.dt.tz is not None:
                result = result.dt.tz_localize(None)
                
            return result
            
        except Exception as e:
            print(f"⚠️  DateTime conversion warning: {e}")
            # Fallback: try string conversion
            try:
                return pd.to_datetime(series.astype(str), errors='coerce')
            except:
                return series
    
    def download_price_data(self, ticker, period="2y"):
        """Download stock price data for Task 2"""
        price_path = PRICES_DIR / f"{ticker}.csv"
        
        # Create directory if it doesn't exist
        PRICES_DIR.mkdir(parents=True, exist_ok=True)
        
        if price_path.exists():
            print(f"📖 Loading existing data for {ticker}...")
            return self._load_price_csv(price_path)
        
        print(f"📥 Downloading {ticker}...")
        
        try:
            # Download data
            stock_data = yf.download(ticker, period=period, progress=False)
            
            if stock_data.empty:
                print(f"❌ No data for {ticker}, generating sample...")
                return self._generate_sample_price_data(ticker)
            
            # Reset index and clean data
            stock_data = stock_data.reset_index()
            stock_data['ticker'] = ticker
            
            # Handle timezone in the date column
            if 'Date' in stock_data.columns:
                stock_data['Date'] = self._safe_datetime_conversion(stock_data['Date'])
            
            # Save to CSV
            stock_data.to_csv(price_path, index=False)
            print(f"✅ Downloaded {ticker}: {len(stock_data)} records")
            
            return stock_data
            
        except Exception as e:
            print(f"❌ Error downloading {ticker}: {e}")
            return self._generate_sample_price_data(ticker)
    
    def load_all_price_data(self):
        """Load price data for all tickers"""
        print("📈 Loading price data for all tickers...")
        
        all_data = []
        for ticker in TICKERS:
            df = self.download_price_data(ticker)
            if df is not None and not df.empty:
                all_data.append(df)
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            print(f"📊 Total price records: {len(combined_df)}")
            return combined_df
        else:
            print("❌ No price data loaded")
            return pd.DataFrame()
    
    def _load_price_csv(self, path):
        """Load price data from CSV with timezone handling"""
        try:
            df = pd.read_csv(path)
            
            # Handle date column with timezone awareness
            date_cols = ['Date', 'date', 'datetime']
            for col in date_cols:
                if col in df.columns:
                    df['date'] = self._safe_datetime_conversion(df[col])
                    break
            
            # Ensure ticker column exists
            if 'ticker' not in df.columns:
                df['ticker'] = path.stem
            
            print(f"✅ Loaded existing price data: {path.stem} ({len(df)} records)")
            return df
            
        except Exception as e:
            print(f"❌ Error loading {path}: {e}")
            return None
    
    def _generate_sample_price_data(self, ticker):
        """Generate sample price data if download fails"""
        print(f"🔧 Generating sample data for {ticker}...")
        
        base_prices = {'AAPL': 150, 'MSFT': 300, 'GOOG': 120, 'AMZN': 130, 'META': 250, 'NVDA': 400}
        base_price = base_prices.get(ticker, 100)
        
        # Generate 2 years of data
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=730),
            end=datetime.now(),
            freq='D'
        )
        
        # Realistic price movement
        returns = np.random.normal(0.0005, 0.018, len(dates))
        prices = base_price * (1 + returns).cumprod()
        
        data = []
        for i, date in enumerate(dates):
            close = prices[i]
            open_price = close * (1 + np.random.normal(0, 0.008))
            high = max(open_price, close) * (1 + abs(np.random.normal(0, 0.012)))
            low = min(open_price, close) * (1 - abs(np.random.normal(0, 0.012)))
            volume = np.random.randint(1000000, 50000000)
            
            data.append({
                'Date': date,
                'Open': open_price,
                'High': high,
                'Low': low,
                'Close': close,
                'Volume': volume,
                'ticker': ticker
            })
        
        df = pd.DataFrame(data)
        price_path = PRICES_DIR / f"{ticker}.csv"
        df.to_csv(price_path, index=False)
        
        print(f"✅ Generated sample data for {ticker}: {len(df)} records")
        return df

# For backward compatibility
def load_news_data():
    loader = DataLoader()
    return loader.load_news_data()