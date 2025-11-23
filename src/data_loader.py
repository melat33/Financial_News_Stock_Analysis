<<<<<<< HEAD
# 📁 src/data_loader.py
import pandas as pd
import os
from src.config import NEWS_FILE

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
=======
# 📁 src/data_loader.py - UPDATED FOR TASK 2
import pandas as pd
import numpy as np
import os
import yfinance as yf
from datetime import datetime, timedelta
from src.config import *
from .config import PRICES_DIR

class DataLoader:
    """
    Enhanced data loader for both news and price data
    Supports Task 1 (News Analysis) and Task 2 (Technical Analysis)
    """
    
    def __init__(self):
        self.news_data = None
        self.price_data = {}
        
    def load_news_data(self):
        """Load news data for sentiment analysis with robust datetime parsing"""
        print("📰 LOADING NEWS DATA...")
        
        try:
            if not os.path.exists(NEWS_FILE):
                print(f"❌ News file not found: {NEWS_FILE}")
                print("💡 Please ensure news data is available")
                return None
                
            # Load with flexible datetime parsing
            df = pd.read_csv(NEWS_FILE)
            
            # Robust datetime parsing - handle multiple formats
            date_parsed = False
            for date_format in ['%Y-%m-%d %H:%M:%S%z', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                try:
                    df['date'] = pd.to_datetime(df['date'], format=date_format)
                    date_parsed = True
                    break
                except:
                    continue
            
            if not date_parsed:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            # Remove any rows with invalid dates
            original_count = len(df)
            df = df.dropna(subset=['date'])
            if len(df) < original_count:
                print(f"⚠️  Removed {original_count - len(df)} rows with invalid dates")
            
            # Filter for our target companies
            df = df[df['stock'].isin(TICKERS)]
            
            print(f"✅ News data loaded: {len(df)} articles")
            print(f"📅 Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
            print(f"🏢 Companies: {df['stock'].nunique()} companies")
            
            if 'publisher' in df.columns:
                print(f"📰 Publishers: {df['publisher'].nunique()}")
            
            self.news_data = df
            return df
            
        except Exception as e:
            print(f"❌ Error loading news: {e}")
            return None
    
    def download_price_data(self, ticker, period="2y", force_download=False):
        """Download stock price data using yfinance"""
        # ✅ CHANGED: Use relative path to ../data/price/
        price_path = f"../data/price/{ticker}.csv"
        
        # ✅ CHANGED: Create directory if it doesn't exist
        os.makedirs(os.path.dirname(price_path), exist_ok=True)
        
        if not force_download and os.path.exists(price_path):
            print(f"📖 Loading existing price data for {ticker}...")
            return self.load_price_csv(price_path)
        
        print(f"📥 Downloading {ticker} price data...")
        
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, auto_adjust=True)
            
            if df.empty:
                print(f"❌ No data downloaded for {ticker}")
                return self.generate_sample_price_data(ticker)
            
            # Reset index and format
            df = df.reset_index()
            df['Date'] = pd.to_datetime(df['Date'])
            df['Stock'] = ticker
            
            # Ensure required columns
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in required_cols:
                if col not in df.columns:
                    print(f"❌ Missing column {col} for {ticker}")
                    return self.generate_sample_price_data(ticker)
            
            # ✅ CHANGED: Save to ../data/price/
            df.to_csv(price_path, index=False)
            print(f"✅ Downloaded {len(df)} records for {ticker} → {price_path}")
            
            return df
            
        except Exception as e:
            print(f"❌ Download error for {ticker}: {e}")
            return self.generate_sample_price_data(ticker)
    
    def load_price_csv(self, path):
        """Load price data from CSV with flexible column handling"""
        try:
            df = pd.read_csv(path)
            
            # Handle date columns
            date_col = None
            for col in ['Date', 'date', 'datetime', 'time']:
                if col in df.columns:
                    date_col = col
                    break
            
            if not date_col:
                raise ValueError(f"No date column in {path}")
            
            df['Date'] = pd.to_datetime(df[date_col])
            
            # Handle column name variations
            col_mapping = {}
            standard_cols = {
                'Open': ['open', 'opening'],
                'High': ['high', 'highest'], 
                'Low': ['low', 'lowest'],
                'Close': ['close', 'closing'],
                'Volume': ['volume', 'vol']
            }
            
            for std_col, variants in standard_cols.items():
                if std_col not in df.columns:
                    for var in variants:
                        if var in df.columns:
                            col_mapping[var] = std_col
                            break
            
            if col_mapping:
                df = df.rename(columns=col_mapping)
            
            return df
            
        except Exception as e:
            print(f"❌ Error loading {path}: {e}")
            return None
    
    def generate_sample_price_data(self, ticker):
        """Generate realistic sample price data for testing"""
        print(f"🔧 Generating sample price data for {ticker}...")
        
        # Base prices for realism
        base_prices = {'AAPL': 150, 'MSFT': 300, 'GOOG': 120, 'AMZN': 130, 'META': 250, 'NVDA': 400}
        base_price = base_prices.get(ticker, 100)
        
        # Generate 2 years of daily data
        dates = pd.date_range(datetime.now() - timedelta(days=730), datetime.now(), freq='D')
        
        # Realistic price series with trends and volatility
        returns = np.random.normal(0.0005, 0.018, len(dates))
        prices = base_price * (1 + returns).cumsum()
        
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
                'Stock': ticker
            })
        
        df = pd.DataFrame(data)
        df['High'] = df[['Open', 'Close', 'High']].max(axis=1)
        df['Low'] = df[['Open', 'Close', 'Low']].min(axis=1)
        
        # ✅ CHANGED: Save to ../data/price/
        price_path = f"../data/price/{ticker}.csv"
        os.makedirs(os.path.dirname(price_path), exist_ok=True)
        df.to_csv(price_path, index=False)
        
        print(f"✅ Generated sample data for {ticker}: {len(df)} records → {price_path}")
        return df
    
    def load_all_price_data(self, force_download=False):
        """Load price data for all tickers"""
        print("📈 LOADING PRICE DATA FOR TECHNICAL ANALYSIS...")
        print("=" * 60)
        
        self.price_data = {}
        success_count = 0
        
        for ticker in TICKERS:
            df = self.download_price_data(ticker, force_download=force_download)
            if df is not None:
                self.price_data[ticker] = df
                success_count += 1
                print(f"   ✅ {ticker}: {len(df)} records")
            else:
                print(f"   ❌ {ticker}: Failed to load data")
        
        print(f"📊 Price data loaded: {success_count}/{len(TICKERS)} companies")
        return self.price_data
    
    def load_technical_indicators(self, ticker):
        """Load pre-computed technical indicators"""
        # ✅ CHANGED: Use relative path
        tech_path = f"../data/processed/technical_indicators/{ticker}_tech.csv"
        
        if os.path.exists(tech_path):
            try:
                df = pd.read_csv(tech_path, parse_dates=['Date'])
                df.set_index('Date', inplace=True)
                print(f"✅ Loaded technical indicators for {ticker}")
                return df
            except Exception as e:
                print(f"❌ Error loading technical indicators for {ticker}: {e}")
                return None
        else:
            print(f"⚠️  Technical indicators not found for {ticker}")
            print("💡 Run technical analysis pipeline first")
            return None
    
    def validate_news_data(self, df):
        """Validate and clean news data for Task 1"""
        print("\n🔍 VALIDATING NEWS DATA QUALITY...")
        
        if df is None:
            return None
        
        # Check required columns
        required_cols = ['date', 'headline', 'stock']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"❌ Missing columns: {missing_cols}")
            return None
        
        # Basic stats
        print(f"📊 Total articles: {len(df):,}")
        print(f"📅 Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
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
    
    def get_data_summary(self):
        """Get comprehensive data summary for both tasks"""
        print("\n📊 COMPREHENSIVE DATA SUMMARY")
        print("=" * 60)
        
        # News data summary
        if self.news_data is not None:
            print("📰 NEWS DATA:")
            print(f"   • Articles: {len(self.news_data):,}")
            print(f"   • Date range: {self.news_data['date'].min().strftime('%Y-%m-%d')} to {self.news_data['date'].max().strftime('%Y-%m-%d')}")
            print(f"   • Companies: {self.news_data['stock'].nunique()}")
        
        # Price data summary  
        if self.price_data:
            print("📈 PRICE DATA:")
            for ticker, df in self.price_data.items():
                print(f"   • {ticker}: {len(df)} records, {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
        
        # Technical indicators summary
        tech_path = "../data/processed/technical_indicators/"
        if os.path.exists(tech_path):
            tech_files = [f for f in os.listdir(tech_path) if f.endswith('_tech.csv')]
            if tech_files:
                print("🔧 TECHNICAL INDICATORS:")
                print(f"   • Available for {len(tech_files)} companies")
        
        print("=" * 60)

# Standalone functions for backward compatibility
def load_news_data():
    """Standalone function for Task 1 compatibility"""
    loader = DataLoader()
    return loader.load_news_data()

def validate_news_data(df):
    """Standalone function for Task 1 compatibility"""
    loader = DataLoader()
    return loader.validate_news_data(df)

# Quick usage examples
if __name__ == "__main__":
    loader = DataLoader()
    
    # Load news data (Task 1)
    news_df = loader.load_news_data()
    if news_df is not None:
        loader.validate_news_data(news_df)
    
    # Load price data (Task 2)  
    price_data = loader.load_all_price_data()
    
    # Get comprehensive summary
    loader.get_data_summary()
>>>>>>> task-2
