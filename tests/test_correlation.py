# tests/test_sentiment_analysis.py
import pytest
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sentiment_analyzer import SentimentAnalyzer

def test_sentiment_analyzer_initialization():
    """Test that sentiment analyzer initializes correctly"""
    analyzer = SentimentAnalyzer()
    assert analyzer is not None

def test_sentiment_analysis():
    """Test sentiment analysis on sample headlines"""
    analyzer = SentimentAnalyzer()
    
    # Test positive sentiment
    positive_score = analyzer.analyze_sentiment("Great earnings report! Stock surges!")
    assert positive_score > 0
    
    # Test negative sentiment  
    negative_score = analyzer.analyze_sentiment("Terrible losses. Company in trouble.")
    assert negative_score < 0
    
    # Test classification
    assert analyzer.classify_sentiment(0.5) == 'positive'
    assert analyzer.classify_sentiment(-0.5) == 'negative'
    assert analyzer.classify_sentiment(0.0) == 'neutral'