import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
    
    def analyze_sentiment(self, news_data):
        try:
            print("   Calculating TextBlob sentiment...")
            results = news_data.copy()
            results['textblob_sentiment'] = results['content'].apply(
                lambda x: TextBlob(str(x)).sentiment.polarity
            )
            print("   Calculating VADER sentiment...")
            results['vader_sentiment'] = results['content'].apply(
                lambda x: self.vader_analyzer.polarity_scores(str(x))['compound']
            )
            return results
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return None
    
    def calculate_daily_sentiment(self, sentiment_results):
        try:
            daily_sentiment = sentiment_results.groupby(['date', 'ticker']).agg({
                'textblob_sentiment': 'mean',
                'vader_sentiment': 'mean',
                'content': 'count'
            }).reset_index()
            daily_sentiment.rename(columns={'content': 'article_count'}, inplace=True)
            return daily_sentiment
        except Exception as e:
            print(f"Error calculating daily sentiment: {e}")
            return None