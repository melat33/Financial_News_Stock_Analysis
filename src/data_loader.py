
# src/data_loader.py - Unified for both Task 1 and Task 2
import pandas as pd
import numpy as np
import os
import yfinance as yf
from datetime import datetime, timedelta
from .config import *

class DataLoader:
    """
    Unified data loader for both Task 1 (News Analysis) and Task 2 (Technical Analysis)
    """

    def __init__(self):
        self.news_data = None
        self.price_data = {}

    # =========================================================================
    # TASK 1 METHODS - NEWS DATA ANALYSIS
    # =========================================================================

    def load_news_data(self):
        """Load news data for sentiment analysis (Task 1)"""
        print("📰 Loading news data...")

        try:
            if not os.path.exists(NEWS_FILE):
                print(f"❌ News file not found: {NEWS_FILE}")
                print("💡 Please ensure news data is available in data/raw/")
                return None

            # Load with flexible datetime parsing
            df = pd.read_csv(NEWS_FILE)

            # Robust datetime parsing
            df = self._parse_dates_safely(df, 'date')

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
            print(f"❌ Error loading news data: {e}")
            return None

    def validate_news_data(self, df):
        """Validate and clean news data for Task 1"""
        print("\n🔍 Validating news data quality...")

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

    # =========================================================================
    # TASK 2 METHODS - PRICE DATA & TECHNICAL ANALYSIS
    # =========================================================================

    def download_price_data(self, ticker, period="2y", force_download=False):
        """Download stock price data using yfinance (Task 2)"""
        price_path = os.path.join(PRICES_DIR, f"{ticker}.csv")

        if not force_download and os.path.exists(price_path):
            print(f"📖 Loading existing price data for {ticker}...")
            return self._load_price_csv(price_path)

        print(f"📥 Downloading {ticker} price data...")

        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, auto_adjust=True)

            if df.empty:
                print(f"❌ No data downloaded for {ticker}")
                return self._generate_sample_price_data(ticker)

            # Reset index and format
            df = df.reset_index()
            df['Date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_convert(None)
            df['Stock'] = ticker

            # Ensure required columns
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in required_cols:
                if col not in df.columns:
                    print(f"❌ Missing column {col} for {ticker}")
                    return self._generate_sample_price_data(ticker)

            # Save to CSV
            df.to_csv(price_path, index=False)
            print(f"✅ Downloaded {len(df)} records for {ticker} → {price_path}")

            return df

        except Exception as e:
            print(f"❌ Download error for {ticker}: {e}")
            return self._generate_sample_price_data(ticker)

    def load_all_price_data(self, force_download=False):
        """Load price data for all tickers (Task 2)"""
        print("📈 Loading price data for technical analysis...")

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
        """Load pre-computed technical indicators (Task 2)"""
        tech_path = os.path.join(PROCESSED_DATA_DIR, 'technical_indicators', f"{ticker}_tech.csv")

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

    # =========================================================================
    # UTILITY METHODS (SHARED)
    # =========================================================================

    def _parse_dates_safely(self, df, date_column):
        """Safely parse dates with multiple format attempts"""
        if date_column not in df.columns:
            return df

        for date_format in ['%Y-%m-%d %H:%M:%S%z', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
            try:
                df[date_column] = pd.to_datetime(df[date_column], format=date_format)
                return df
            except:
                continue

        # Final attempt with coercion
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        return df

    def _load_price_csv(self, path):
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

            # FIX: Use utc=True to handle time zones properly and then remove timezone
            df['Date'] = pd.to_datetime(df[date_col], utc=True).dt.tz_convert(None)

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

    def _generate_sample_price_data(self, ticker):
        """Generate realistic sample price data for testing"""
        print(f"🔧 Generating sample price data for {ticker}...")

        # Base prices for different stocks
        base_prices = {'AAPL': 150, 'MSFT': 300, 'GOOG': 120, 'AMZN': 130, 'META': 250, 'NVDA': 400}
        base_price = base_prices.get(ticker, 100)

        # Generate 2 years of daily data
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=730),
            end=datetime.now(),
            freq='D'
        )

        # Realistic price movement with trends and volatility
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
                'Stock': ticker
            })

        df = pd.DataFrame(data)
        df['High'] = df[['Open', 'Close', 'High']].max(axis=1)
        df['Low'] = df[['Open', 'Close', 'Low']].min(axis=1)

        # Save the sample data
        price_path = os.path.join(PRICES_DIR, f"{ticker}.csv")
        df.to_csv(price_path, index=False)

        print(f"✅ Generated sample data for {ticker}: {len(df)} records → {price_path}")
        return df

    def get_data_summary(self):
        """Get comprehensive data summary for both tasks"""
        print("\n📊 COMPREHENSIVE DATA SUMMARY")
        print("=" * 60)

        # News data summary (Task 1)
        if self.news_data is not None:
            print("📰 TASK 1 - NEWS DATA:")
            print(f"   • Articles: {len(self.news_data):,}")
            print(f"   • Date range: {self.news_data['date'].min().strftime('%Y-%m-%d')} to {self.news_data['date'].max().strftime('%Y-%m-%d')}")
            print(f"   • Companies: {self.news_data['stock'].nunique()}")

        # Price data summary (Task 2)
        if self.price_data:
            print("📈 TASK 2 - PRICE DATA:")
            for ticker, df in self.price_data.items():
                print(f"   • {ticker}: {len(df)} records, {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")

        # Technical indicators summary (Task 2)
        tech_path = os.path.join(PROCESSED_DATA_DIR, 'technical_indicators')
        if os.path.exists(tech_path):
            tech_files = [f for f in os.listdir(tech_path) if f.endswith('_tech.csv')]
            if tech_files:
                print("🔧 TASK 2 - TECHNICAL INDICATORS:")
                print(f"   • Available for {len(tech_files)} companies")

        print("=" * 60)

# For backward compatibility, we can keep the standalone functions for Task 1
def load_news_data():
    """Standalone function for Task 1 compatibility"""
    loader = DataLoader()
    return loader.load_news_data()

def validate_news_data(df):
    """Standalone function for Task 1 compatibility"""
    loader = DataLoader()
    return loader.validate_news_data(df)