import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from correlation_analyzer import CorrelationAnalyzer
from sentiment import SentimentAnalyzer
from merge_and_features import DataMerger

class TestCorrelationAnalysis(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.correlation_analyzer = CorrelationAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.data_merger = DataMerger()
        
        # Create sample data for testing
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        
        self.sample_news = pd.DataFrame({
            'date': dates,
            'headline': [f'Test headline {i}' for i in range(100)],
            'textblob_sentiment': np.random.normal(0, 0.3, 100),
            'vader_sentiment': np.random.normal(0, 0.3, 100),
            'combined_sentiment': np.random.normal(0, 0.3, 100),
            'sentiment_category': np.random.choice(['positive', 'negative', 'neutral'], 100)
        })
        
        self.sample_stock = pd.DataFrame({
            'date': dates,
            'close': 100 + np.cumsum(np.random.normal(0, 1, 100)),
            'daily_return': np.random.normal(0, 1, 100)
        })
    
    def test_correlation_metrics(self):
        """Test correlation calculation"""
        metrics = self.correlation_analyzer.calculate_correlation_metrics(
            self.sample_stock, 'daily_return', 'daily_return'
        )
        
        self.assertIsNotNone(metrics)
        self.assertIn('pearson_correlation', metrics)
        self.assertIn('pearson_p_value', metrics)
        self.assertIn('correlation_strength', metrics)
    
    def test_sentiment_analysis(self):
        """Test sentiment analysis functionality"""
        test_headlines = [
            "Great company reports amazing profits!",
            "Terrible losses reported by company",
            "Company announces regular quarterly results"
        ]
        
        for headline in test_headlines:
            sentiment = self.sentiment_analyzer.textblob_sentiment(headline)
            self.assertIsInstance(sentiment, float)
            self.assertTrue(-1 <= sentiment <= 1)
    
    def test_data_merger(self):
        """Test data merging functionality"""
        merged_data = self.data_merger.merge_sentiment_returns(
            self.sample_news, self.sample_stock
        )
        
        self.assertIsInstance(merged_data, pd.DataFrame)
        self.assertTrue(len(merged_data) > 0)
        self.assertIn('daily_return', merged_data.columns)
        self.assertIn('combined_sentiment', merged_data.columns)
    
    def test_correlation_interpretation(self):
        """Test correlation strength interpretation"""
        test_cases = [
            (0.8, "Very Strong"),
            (0.6, "Strong"), 
            (0.4, "Moderate"),
            (0.2, "Weak"),
            (0.05, "Very Weak"),
            (-0.7, "Very Strong")
        ]
        
        for correlation, expected_strength in test_cases:
            strength = self.correlation_analyzer._interpret_correlation_strength(correlation)
            self.assertEqual(strength, expected_strength)

if __name__ == '__main__':
    unittest.main()