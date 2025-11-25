# src/text_analyzer.py
import pandas as pd
import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pathlib import Path

# Import config using absolute path to avoid circular imports
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from src.config import SENTIMENT_DIR, SENTIMENT_CONFIG

class TextAnalyzer:
    """Sentiment analysis for financial news"""
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
    
    def analyze_sentiment(self, news_df):
        """Perform comprehensive sentiment analysis on news headlines"""
        print("😊 Analyzing news sentiment...")
        
        if news_df.empty:
            print("❌ No news data to analyze")
            return pd.DataFrame()
        
        # Make a copy to avoid modifying original
        df = news_df.copy()
        
        # TextBlob sentiment
        print("   Calculating TextBlob sentiment...")
        df['textblob_sentiment'] = df['headline'].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity if pd.notna(x) else 0
        )
        
        # VADER sentiment
        print("   Calculating VADER sentiment...")
        df['vader_sentiment'] = df['headline'].apply(
            lambda x: self.vader_analyzer.polarity_scores(str(x))['compound'] if pd.notna(x) else 0
        )
        
        # Combined sentiment (average of both)
        df['combined_sentiment'] = (df['textblob_sentiment'] + df['vader_sentiment']) / 2
        
        # Sentiment categories
        df['sentiment_category'] = df['combined_sentiment'].apply(self._categorize_sentiment)
        
        print(f"✅ Sentiment analysis completed: {len(df)} articles")
        print(f"   Sentiment range: {df['combined_sentiment'].min():.3f} to {df['combined_sentiment'].max():.3f}")
        
        return df
    
    def calculate_daily_sentiment(self, sentiment_df):
        """Calculate daily sentiment aggregates by company"""
        print("📊 Calculating daily sentiment aggregates...")
        
        daily_sentiment = sentiment_df.groupby(['date', 'stock']).agg({
            'textblob_sentiment': ['mean', 'count'],
            'vader_sentiment': ['mean', 'count'],
            'combined_sentiment': ['mean', 'std', 'count'],
            'sentiment_category': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Neutral'
        }).round(4)
        
        # Flatten column names
        daily_sentiment.columns = [
            'textblob_mean', 'textblob_count',
            'vader_mean', 'vader_count', 
            'combined_mean', 'combined_std', 'combined_count',
            'dominant_category'
        ]
        
        daily_sentiment = daily_sentiment.reset_index()
        
        # Save daily sentiment
        SENTIMENT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = SENTIMENT_DIR / 'daily_sentiment.csv'
        daily_sentiment.to_csv(output_path, index=False)
        print(f"💾 Daily sentiment saved: {output_path}")
        
        return daily_sentiment
    
    def _categorize_sentiment(self, score):
        """Categorize sentiment score"""
        if score >= SENTIMENT_CONFIG['positive_threshold']:
            return "Positive"
        elif score <= SENTIMENT_CONFIG['negative_threshold']:
            return "Negative"
        else:
            return "Neutral"

# Create and export the instance
text_analyzer = TextAnalyzer()