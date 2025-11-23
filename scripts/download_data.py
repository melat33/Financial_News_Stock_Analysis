<<<<<<< HEAD
# 📁 scripts/download_data.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from src.config import RAW_DIR, TICKERS

def create_sample_news_data():
    """Create realistic sample news data for EDA analysis focused on 6 companies"""
    news_file = os.path.join(RAW_DIR, "raw_analyst_ratings.csv")
    
    if os.path.exists(news_file):
        print("✅ News file already exists")
        return
    
    print("📰 CREATING SAMPLE NEWS DATA FOR 6 COMPANIES...")
    print(f"🏢 Companies: {TICKERS}")
    
    # Sample publishers (mix of organizations and emails)
    publishers = [
        'Bloomberg', 'Reuters', 'CNBC', 'Wall Street Journal',
        'analyst@morganstanley.com', 'research@goldmansachs.com',
        'markets@bankofamerica.com', 'equity@citigroup.com'
    ]
    
    # Generate sample data
    sample_news = []
    
    # Date range for sample data
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
    
    for i, date in enumerate(dates):
        if np.random.random() > 0.3:  # 70% chance of having news each day
            num_articles = np.random.poisson(8)  # Average 8 articles per news day
            
            for j in range(num_articles):
                company = np.random.choice(TICKERS)
                publisher = np.random.choice(publishers)
                
                # Company-specific headline templates
                headline_templates = {
                    "AAPL": [
                        f"AAPL unveils new iPhone with {np.random.choice(['5G', 'AI', 'camera'])} features",
                        f"Apple Q{np.random.randint(1,5)} earnings {np.random.choice(['beat', 'miss'])} expectations",
                        f"AAPL stock {np.random.choice(['rises', 'falls'])} on {np.random.choice(['iPhone sales', 'services growth', 'China market'])} news"
                    ],
                    "AMZN": [
                        f"Amazon AWS growth {np.random.choice(['accelerates', 'slows'])} in Q{np.random.randint(1,5)}",
                        f"AMZN {np.random.choice(['expands', 'cuts'])} {np.random.choice(['delivery network', 'cloud services', 'workforce'])}",
                        f"Amazon Q{np.random.randint(1,5)} revenue {np.random.choice(['exceeds', 'misses'])} estimates"
                    ],
                    "GOOG": [
                        f"Google {np.random.choice(['launches', 'updates'])} {np.random.choice(['AI features', 'search algorithm', 'cloud platform'])}",
                        f"Alphabet Q{np.random.randint(1,5)} {np.random.choice(['ad revenue', 'cloud revenue'])} {np.random.choice(['surges', 'declines'])}",
                        f"GOOGL stock reacts to {np.random.choice(['regulatory', 'antitrust', 'privacy'])} news"
                    ],
                    "META": [
                        f"Meta Platforms {np.random.choice(['introduces', 'expands'])} {np.random.choice(['metaverse', 'VR', 'AI'])} initiatives",
                        f"Facebook parent Q{np.random.randint(1,5)} {np.random.choice(['user growth', 'ad revenue'])} {np.random.choice(['strong', 'weak'])}",
                        f"META {np.random.choice(['partners with', 'acquires'])} {np.random.choice(['AI startup', 'gaming company'])}"
                    ],
                    "MSFT": [
                        f"Microsoft Azure growth {np.random.choice(['accelerates', 'moderates'])} in Q{np.random.randint(1,5)}",
                        f"MSFT {np.random.choice(['announces', 'launches'])} new {np.random.choice(['Windows', 'Office', 'cloud'])} features",
                        f"Microsoft Q{np.random.randint(1,5)} earnings {np.random.choice(['beat', 'meet', 'miss'])} expectations"
                    ],
                    "NVDA": [
                        f"NVIDIA {np.random.choice(['reports', 'forecasts'])} {np.random.choice(['strong', 'weak'])} {np.random.choice(['AI chip', 'gaming'])} demand",
                        f"NVDA stock {np.random.choice(['surges', 'drops'])} on {np.random.choice(['earnings', 'guidance', 'partnership'])} news",
                        f"NVIDIA Q{np.random.randint(1,5)} {np.random.choice(['data center', 'gaming'])} revenue {np.random.choice(['exceeds', 'misses'])} estimates"
                    ]
                }
                
                # Get company-specific headlines
                company_headlines = headline_templates.get(company, [
                    f"{company} Q{np.random.randint(1,5)} earnings {np.random.choice(['beat', 'miss'])} expectations",
                    f"Analyst {np.random.choice(['upgrades', 'downgrades'])} {company} to {np.random.choice(['Buy', 'Sell', 'Hold'])}",
                    f"{company} stock {np.random.choice(['rises', 'falls'])} on {np.random.choice(['news', 'earnings', 'guidance'])}"
                ])
                
                headline = np.random.choice(company_headlines)
                
                sample_news.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'stock': company,
                    'headline': headline,
                    'publisher': publisher
                })
    
    # Create DataFrame and save
    news_df = pd.DataFrame(sample_news)
    news_df.to_csv(news_file, index=False)
    
    print(f"✅ Sample news data created: {news_file}")
    print(f"   📰 {len(news_df)} total articles")
    print(f"   🏢 {news_df['publisher'].nunique()} unique publishers")
    print(f"   💼 Companies covered: {sorted(news_df['stock'].unique())}")
    print(f"   📅 Date range: {news_df['date'].min()} to {news_df['date'].max()}")

def main():
    """Main function to create sample data for 6 companies"""
    print("🚀 TASK 1: CREATING SAMPLE NEWS DATA FOR 6 COMPANIES")
    print("=" * 60)
    print(f"📊 Companies: {TICKERS}")
    
    # Create directory
    os.makedirs(RAW_DIR, exist_ok=True)
    
    # Create sample data
    create_sample_news_data()
    
    print("\n🎉 DATA READY FOR EDA ANALYSIS!")
    print("💡 Next: Run python scripts/run_eda.py to start analysis")

if __name__ == "__main__":
    main()
=======
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
>>>>>>> task-2
