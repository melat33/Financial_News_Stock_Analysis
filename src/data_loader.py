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