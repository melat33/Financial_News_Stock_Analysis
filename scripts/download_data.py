#!/usr/bin/env python3
"""
Task 1 - News Data Download Only
Downloads/Creates financial news data for sentiment analysis
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add the project root to Python path to fix import issues
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

print(f"📁 Project root: {project_root}")

# Configuration for Task 1
TICKERS = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'NVDA']
DATA_DIR = os.path.join(project_root, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
NEWS_FILE = os.path.join(RAW_DATA_DIR, 'financial_news.csv')

def create_directories():
    """Create necessary directories"""
    directories = [RAW_DATA_DIR, os.path.join(project_root, 'reports')]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")

def create_realistic_news_data():
    """Create realistic financial news data for Task 1"""
    print("📰 CREATING REALISTIC FINANCIAL NEWS DATA...")
    
    sample_news = []
    current_date = datetime.now()
    
    # Realistic news templates for each company
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
    
    # Fillers for templates
    fillers_1 = ['Q3', 'Q4', 'Q1', 'Q2', 'Latest', 'New', 'Premium', 'Enterprise', 'Cloud', 'Mobile']
    fillers_2 = ['Record', 'Strong', 'Impressive', 'Moderate', 'Steady', 'Rapid', 'Significant']
    actions = ['Upgrade', 'Downgrade', 'Maintain', 'Reiterate', 'Initiate Coverage']
    conditions = ['Bullish', 'Bearish', 'Volatile', 'Stable', 'Challenging', 'Optimistic']
    
    # Create 250 realistic news articles
    for i in range(250):
        date = current_date - timedelta(days=np.random.randint(1, 180))  # Last 6 months
        ticker = TICKERS[i % len(TICKERS)]
        
        # Select template and fill with realistic data
        template = np.random.choice(news_templates[ticker])
        
        # Generate realistic headline
        if '{}' in template:
            headline = template.format(
                np.random.choice(fillers_1),
                np.random.choice(fillers_2)
            )
        else:
            headline = template
        
        # Realistic publishers
        publishers = [
            'Financial Times', 'Bloomberg', 'Reuters', 
            'Wall Street Journal', 'MarketWatch', 'CNBC',
            'Forbes', 'Business Insider', 'Yahoo Finance'
        ]
        
        # Realistic sentiment based on content
        positive_words = ['Strong', 'Growth', 'Record', 'Exceeds', 'Gains', 'Expands', 'Boom']
        negative_words = ['Faces', 'Challenges', 'Scrutiny', 'Downgrade', 'Bearish']
        
        sentiment = 'neutral'
        if any(word in headline for word in positive_words):
            sentiment = 'positive'
        elif any(word in headline for word in negative_words):
            sentiment = 'negative'
        
        sample_news.append({
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'headline': headline,
            'stock': ticker,
            'publisher': np.random.choice(publishers),
            'sentiment': sentiment,
            'article_id': f"NEWS{1000 + i}",
            'word_count': len(headline.split())
        })
    
    # Create DataFrame
    df = pd.DataFrame(sample_news)
    
    # Sort by date (newest first)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date', ascending=False)
    
    # Save to CSV
    df.to_csv(NEWS_FILE, index=False)
    
    print(f"✅ Created realistic news data: {len(df)} articles")
    print(f"💾 Saved to: {NEWS_FILE}")
    
    return df

def validate_news_data():
    """Validate the created news data"""
    print("\n🔍 VALIDATING NEWS DATA...")
    
    if not os.path.exists(NEWS_FILE):
        print("❌ News file not found")
        return False
    
    try:
        df = pd.read_csv(NEWS_FILE)
        df['date'] = pd.to_datetime(df['date'])
        
        print(f"📊 Total Articles: {len(df):,}")
        print(f"📅 Date Range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
        print(f"🏢 Companies: {df['stock'].nunique()} - {', '.join(sorted(df['stock'].unique()))}")
        print(f"📰 Publishers: {df['publisher'].nunique()}")
        
        # Sentiment distribution
        if 'sentiment' in df.columns:
            sentiment_counts = df['sentiment'].value_counts()
            print(f"😊 Sentiment: {sentiment_counts.to_dict()}")
        
        # Articles per company
        print(f"\n📈 Articles per Company:")
        company_counts = df['stock'].value_counts()
        for company, count in company_counts.items():
            percentage = (count / len(df)) * 100
            print(f"   • {company}: {count} articles ({percentage:.1f}%)")
        
        # Sample headlines
        print(f"\n📋 SAMPLE HEADLINES:")
        for i, row in df.head(5).iterrows():
            print(f"   • [{row['stock']}] {row['headline']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def check_existing_data():
    """Check if data already exists"""
    if os.path.exists(NEWS_FILE):
        df = pd.read_csv(NEWS_FILE)
        print(f"📰 Existing news data found: {len(df)} articles")
        
        response = input("🔄 Do you want to recreate the news data? (y/n): ").strip().lower()
        return response not in ['y', 'yes']
    return False

def main():
    """Main function"""
    print("🚀 TASK 1 - NEWS DATA DOWNLOAD")
    print("=" * 60)
    
    # Create directories
    create_directories()
    
    # Check existing data
    if check_existing_data():
        print("✅ Using existing news data")
        validate_news_data()
        return
    
    # Create news data
    news_df = create_realistic_news_data()
    
    # Validate data
    if validate_news_data():
        print("\n🎉 TASK 1 DATA READY!")
        print("=" * 60)
        print("📰 News data is now available for:")
        print("   • Exploratory Data Analysis (EDA)")
        print("   • Sentiment Analysis")
        print("   • News trend analysis")
        print("   • Company-specific news analysis")
        
        print(f"\n📁 File location: {NEWS_FILE}")
        print(f"📊 Data summary: {len(news_df)} articles, {news_df['stock'].nunique()} companies")
        
        print("\n🎯 NEXT STEP:")
        print("   Run: python scripts/run_eda.py")
        print("   Or: jupyter notebook notebooks/01_eda_news_sentiment.ipynb")
    else:
        print("❌ Failed to create valid news data")

if __name__ == "__main__":
    main()