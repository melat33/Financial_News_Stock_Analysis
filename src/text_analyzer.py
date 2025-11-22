import pandas as pd
import numpy as np
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from src.config import TICKERS

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
except:
    print("⚠️  NLTK downloads failed - using fallback methods")

class TextAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.sia = SentimentIntensityAnalyzer()
        
        # Company-specific keywords for topic modeling
        self.company_keywords = {
            "AAPL": ['iphone', 'ios', 'mac', 'ipad', 'app store', 'tim cook', 'apple watch'],
            "AMZN": ['aws', 'amazon web services', 'prime', 'bezos', 'ecommerce', 'delivery'],
            "GOOG": ['google', 'alphabet', 'search', 'youtube', 'android', 'sundar pichai'],
            "META": ['facebook', 'instagram', 'whatsapp', 'metaverse', 'zuckerberg', 'vr'],
            "MSFT": ['microsoft', 'azure', 'windows', 'office', 'satya nadella', 'cloud'],
            "NVDA": ['nvidia', 'gpu', 'ai chips', 'cuda', 'jensen huang', 'graphics']
        }
        
        # General financial keywords
        self.financial_keywords = [
            'earnings', 'revenue', 'profit', 'loss', 'growth', 'dividend', 
            'stock', 'share', 'price', 'target', 'upgrade', 'downgrade',
            'quarter', 'q1', 'q2', 'q3', 'q4', 'guidance', 'forecast',
            'beat', 'miss', 'expectations', 'analyst', 'rating', 'buy', 'sell'
        ]

    def clean_text(self, text):
        """Clean and preprocess text"""
        if pd.isna(text):
            return ""
        
        text = str(text).lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        text = re.sub(r'\d+', '', text)  # Remove numbers
        return text.strip()

    def extract_keywords(self, text, top_n=10):
        """Extract top keywords from text"""
        text = self.clean_text(text)
        tokens = word_tokenize(text)
        words = [word for word in tokens if word not in self.stop_words and len(word) > 2]
        return Counter(words).most_common(top_n)

    def analyze_sentiment(self, text):
        """Analyze sentiment using VADER"""
        scores = self.sia.polarity_scores(text)
        return {
            'sentiment_compound': scores['compound'],
            'sentiment_positive': scores['pos'],
            'sentiment_negative': scores['neg'],
            'sentiment_neutral': scores['neu']
        }

    def detect_topics(self, text, company):
        """Detect topics in headlines"""
        text_lower = text.lower()
        topics = []
        
        # Check company-specific topics
        for keyword in self.company_keywords.get(company, []):
            if keyword in text_lower:
                topics.append(keyword)
        
        # Check financial topics
        for keyword in self.financial_keywords:
            if keyword in text_lower:
                topics.append(keyword)
        
        return topics

    def analyze_headline_features(self, df):
        """Add text analysis features to dataframe"""
        print("🔤 Analyzing headline features...")
        
        # Basic text features
        df['headline_clean'] = df['headline'].apply(self.clean_text)
        df['headline_length'] = df['headline'].str.len()
        df['word_count'] = df['headline'].str.split().str.len()
        df['avg_word_length'] = df['headline_clean'].str.split().apply(
            lambda x: np.mean([len(word) for word in x]) if x else 0
        )
        
        # Sentiment analysis
        sentiment_scores = df['headline'].apply(self.analyze_sentiment)
        sentiment_df = pd.json_normalize(sentiment_scores)
        df = pd.concat([df, sentiment_df], axis=1)
        
        # Topic detection
        df['topics'] = df.apply(
            lambda row: self.detect_topics(row['headline'], row['stock']), axis=1
        )
        df['topic_count'] = df['topics'].str.len()
        
        print(f"✅ Added {len(sentiment_df.columns)} text features")
        return df

    def get_company_keyword_summary(self, df):
        """Get keyword summary by company"""
        print("\n🏷️  Generating keyword analysis by company...")
        
        keyword_summary = {}
        for company in TICKERS:
            company_news = df[df['stock'] == company]
            all_text = ' '.join(company_news['headline_clean'].astype(str))
            keywords = self.extract_keywords(all_text, top_n=15)
            keyword_summary[company] = keywords
            
            print(f"   {company}: {[kw[0] for kw in keywords[:5]]}")
        
        return keyword_summary