# scripts/generate_news_matching_stock_dates.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import TICKERS, NEWS_FILE, PRICES_DIR

def get_stock_trading_days():
    """Get the actual trading days from stock data"""
    print("📅 Getting stock trading days...")
    
    all_trading_days = set()
    for ticker in TICKERS:
        price_file = PRICES_DIR / f"{ticker}.csv"
        if price_file.exists():
            df = pd.read_csv(price_file)
            if 'Date' in df.columns:
                # Use utc=True and then remove timezone for consistency
                dates = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
                all_trading_days.update(dates.dt.strftime('%Y-%m-%d').tolist())
    
    trading_days_list = sorted(list(all_trading_days))
    print(f"✅ Found {len(trading_days_list)} unique trading days")
    print(f"   Date range: {trading_days_list[0]} to {trading_days_list[-1]}")
    
    return trading_days_list

def create_news_on_trading_days():
    """Create news data that exactly matches stock trading days"""
    print("📰 Creating news data on actual trading days...")
    
    # Get ACTUAL trading days from stock data
    trading_days = get_stock_trading_days()
    
    if not trading_days:
        print("❌ No trading days found")
        return pd.DataFrame()
    
    sample_news = []
    
    # News templates
    news_templates = {
        'AAPL': [
            "Apple Reports Strong iPhone Sales in Q{} {}",
            "Apple Announces New {} with Enhanced Features", 
            "Analysts {} Apple Stock Amid {} Market Conditions",
            "Apple {} Exceeds Expectations in {} Markets",
            "Apple Faces {} Challenges in {} Division"
        ],
        'MSFT': [
            "Microsoft {} Cloud Services Show {} Growth",
            "Windows {} Update Brings New {} Features",
            "Microsoft {} Division Reports {} Results",
            "Analysts {} Microsoft Amid {} Developments",
            "Microsoft Expands {} Partnerships in {}"
        ],
        'GOOG': [
            "Google {} Revenue Grows {}% in Latest Report",
            "Alphabet Announces {} Initiatives for {}",
            "Google {} Faces {} Regulatory Scrutiny",
            "Analysts {} Google Stock After {} Announcement",
            "Google Expands {} Services to {} Markets"
        ],
        'AMZN': [
            "Amazon {} Sales Surge {}% in Quarter", 
            "AWS {} Services Experience {} Growth",
            "Amazon Expands {} Delivery in {} Regions",
            "Analysts {} Amazon Amid {} Market Trends",
            "Amazon {} Division Launches {} Features"
        ],
        'META': [
            "Meta {} Platform Gains {} Million New Users",
            "Facebook Parent Reports {} in {} Revenue",
            "Meta {} Initiative Shows {} Progress",
            "Analysts {} Meta Stock After {} Results",
            "Meta Expands {} Services to {} Countries"
        ],
        'NVDA': [
            "NVIDIA {} Chips Drive {}% Revenue Growth",
            "AI Boom Fuels NVIDIA {} Sales in {}",
            "NVIDIA Announces {} Partnerships for {}",
            "Analysts {} NVIDIA Amid {} Market Demand",
            "NVIDIA {} Technology Adopted by {} Companies"
        ]
    }
    
    fillers_1 = ['Q3', 'Q4', 'Q1', 'Q2', 'Latest', 'New', 'Premium', 'Enterprise']
    fillers_2 = ['Record', 'Strong', 'Impressive', 'Moderate', 'Steady', 'Significant']
    publishers = ['Financial Times', 'Bloomberg', 'Reuters', 'Wall Street Journal', 'CNBC']
    
    # Create multiple articles per trading day to ensure overlap
    articles_per_day = 3
    total_articles = min(200, len(trading_days) * articles_per_day)
    
    print(f"📝 Generating {total_articles} articles across {len(trading_days)} trading days...")
    
    article_count = 0
    used_dates = set()
    
    # Distribute articles across trading days
    for i in range(total_articles):
        # Pick a trading day (spread them out)
        day_index = i % len(trading_days)
        trading_date = trading_days[day_index]
        
        # Pick a random company
        ticker = TICKERS[i % len(TICKERS)]
        
        template = np.random.choice(news_templates[ticker])
        headline = template.format(
            np.random.choice(fillers_1),
            np.random.choice(fillers_2)
        )
        
        # Realistic sentiment
        positive_words = ['Strong', 'Growth', 'Record', 'Exceeds', 'Gains', 'Expands']
        negative_words = ['Faces', 'Challenges', 'Scrutiny', 'Downgrade']
        
        sentiment = 'neutral'
        if any(word in headline for word in positive_words):
            sentiment = 'positive'
        elif any(word in headline for word in negative_words):
            sentiment = 'negative'
        
        # Add time to the date
        full_datetime = f"{trading_date} {np.random.randint(9, 18):02d}:00:00"
        
        sample_news.append({
            'date': full_datetime,
            'headline': headline,
            'stock': ticker,
            'publisher': np.random.choice(publishers),
            'sentiment': sentiment,
            'article_id': f"NEWS{1000 + article_count}",
            'word_count': len(headline.split())
        })
        
        used_dates.add(trading_date)
        article_count += 1
    
    # Create DataFrame
    df = pd.DataFrame(sample_news)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date', ascending=False)
    
    # Save to CSV
    NEWS_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(NEWS_FILE, index=False)
    
    print(f"✅ Created news data: {len(df)} articles")
    print(f"💾 Saved to: {NEWS_FILE}")
    print(f"📅 Date range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"📊 Articles distributed across {len(used_dates)} unique trading days")
    
    return df

def main():
    """Main function - Generate news data that exactly matches stock trading days"""
    print("🚀 GENERATING NEWS DATA THAT MATCHES STOCK TRADING DAYS")
    print("=" * 60)
    
    # Delete existing news file to ensure fresh data
    if NEWS_FILE.exists():
        NEWS_FILE.unlink()
        print("🗑️  Deleted existing news file")
    
    # Create new news data
    news_df = create_news_on_trading_days()
    
    print(f"\n🎉 NEWS DATA GENERATION COMPLETED!")
    print(f"📊 {len(news_df)} articles created")
    print(f"📅 Date range: {news_df['date'].min().strftime('%Y-%m-%d')} to {news_df['date'].max().strftime('%Y-%m-%d')}")
    
    print("\n🎯 NEXT: Run correlation analysis")
    print("   python scripts/run_correlation_analysis.py")

if __name__ == "__main__":
    main()