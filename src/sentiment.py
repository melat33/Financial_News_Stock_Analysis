import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import SENTIMENT_DIR, PROCESSED_DIR

# Then in your save methods, use:
output_path = os.path.join(PROCESSED_DIR, "news_with_sentiment.csv")
import pandas as pd
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import logging

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

class SentimentAnalyzer:
    """
    Comprehensive sentiment analysis for financial news
    """
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.logger = logging.getLogger(__name__)
    
    def textblob_sentiment(self, text):
        """Calculate sentiment using TextBlob"""
        if pd.isna(text) or text == '':
            return 0.0
        
        analysis = TextBlob(str(text))
        return analysis.sentiment.polarity
    
    def vader_sentiment(self, text):
        """Calculate sentiment using VADER (specifically for short texts)"""
        if pd.isna(text) or text == '':
            return 0.0
        
        scores = self.sia.polarity_scores(str(text))
        return scores['compound']
    
    def analyze_news_sentiment(self, news_df, text_column='headline'):
        """
        Perform sentiment analysis on news dataframe
        
        Args:
            news_df (pd.DataFrame): News data with headlines
            text_column (str): Column name containing text to analyze
            
        Returns:
            pd.DataFrame: DataFrame with sentiment scores
        """
        self.logger.info("Performing sentiment analysis on news data...")
        
        # Make a copy to avoid modifying original
        result_df = news_df.copy()
        
        # Calculate both sentiment scores
        result_df['textblob_sentiment'] = result_df[text_column].apply(self.textblob_sentiment)
        result_df['vader_sentiment'] = result_df[text_column].apply(self.vader_sentiment)
        
        # Combined sentiment (average of both)
        result_df['combined_sentiment'] = (result_df['textblob_sentiment'] + result_df['vader_sentiment']) / 2
        
        # Categorical sentiment
        result_df['sentiment_category'] = result_df['combined_sentiment'].apply(
            lambda x: 'positive' if x > 0.1 else 'negative' if x < -0.1 else 'neutral'
        )
        
        self.logger.info(f"Sentiment analysis completed. Sample scores: {result_df['combined_sentiment'].head().tolist()}")
        
        return result_df

# Singleton instance for easy import
sentiment_analyzer = SentimentAnalyzer()