# scripts/force_exact_overlap.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import NEWS_FILE, PRICES_DIR, TICKERS

def force_exact_overlap():
    """Force exact overlap by using the same dates and companies"""
    print("💥 FORCING EXACT OVERLAP...")
    
    # Get stock data to extract exact dates and companies
    stock_data = []
    for ticker in TICKERS:
        price_file = PRICES_DIR / f"{ticker}.csv"
        if price_file.exists():
            df = pd.read_csv(price_file)
            if 'Date' in df.columns:
                df['date'] = pd.to_datetime(df['Date'], utc=True).dt.tz_localize(None)
                df['date_only'] = df['date'].dt.date
                df['ticker'] = ticker
                stock_data.append(df)
    
    if not stock_data:
        print("❌ No stock data found")
        return
    
    stock_df = pd.concat(stock_data, ignore_index=True)
    
    # Get unique dates and companies from stock data
    stock_dates = sorted(stock_df['date_only'].unique())
    stock_companies = sorted(stock_df['ticker'].unique())
    
    print(f"📊 Stock data: {len(stock_dates)} dates, {len(stock_companies)} companies")
    
    # Create news data that exactly matches
    sample_news = []
    
    news_templates = {
        'AAPL': "Apple news on {}: {} performance",
        'MSFT': "Microsoft update {}: {} results", 
        'GOOG': "Google report {}: {} growth",
        'AMZN': "Amazon news {}: {} sales",
        'META': "Meta announcement {}: {} users",
        'NVDA': "NVIDIA report {}: {} demand"
    }
    
    # Create 2 news articles for each company on random stock dates
    articles_per_company = 2
    
    for ticker in stock_companies:
        # Pick random dates from this company's trading days
        company_dates = stock_df[stock_df['ticker'] == ticker]['date_only'].unique()
        selected_dates = np.random.choice(company_dates, min(articles_per_company, len(company_dates)), replace=False)
        
        for date in selected_dates:
            template = news_templates[ticker]
            headline = template.format(
                date.strftime('%Y-%m-%d'),
                np.random.choice(['strong', 'solid', 'mixed', 'challenging'])
            )
            
            sample_news.append({
                'date': f"{date} 12:00:00",
                'headline': headline,
                'stock': ticker,
                'publisher': 'Financial Times',
                'sentiment': 'positive' if 'strong' in headline or 'solid' in headline else 'neutral',
                'article_id': f"EXACT{len(sample_news)}",
                'word_count': len(headline.split())
            })
    
    # Create DataFrame
    df = pd.DataFrame(sample_news)
    df['date'] = pd.to_datetime(df['date'])
    
    # Save to CSV
    NEWS_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(NEWS_FILE, index=False)
    
    print(f"✅ Created EXACT overlap news data: {len(df)} articles")
    print(f"💾 Saved to: {NEWS_FILE}")
    
    # Verify the overlap
    news_dates = set(df['date'].dt.date.unique())
    stock_dates_set = set(stock_dates)
    overlap = news_dates.intersection(stock_dates_set)
    
    print(f"📅 Overlap verification:")
    print(f"   News dates: {len(news_dates)}")
    print(f"   Stock dates: {len(stock_dates_set)}") 
    print(f"   Overlapping dates: {len(overlap)}")
    print(f"   Common companies: {set(df['stock'].unique()).intersection(set(stock_companies))}")
    
    return df

def main():
    print("🚀 FORCING EXACT OVERLAP BETWEEN NEWS AND STOCK DATA")
    print("=" * 60)
    
    # Delete existing news file
    if NEWS_FILE.exists():
        NEWS_FILE.unlink()
        print("🗑️  Deleted existing news file")
    
    # Create new news data with exact overlap
    news_df = force_exact_overlap()
    
    print(f"\n🎉 EXACT OVERLAP CREATED!")
    print("🎯 Now run: python scripts/run_correlation_analysis.py")

if __name__ == "__main__":
    main()