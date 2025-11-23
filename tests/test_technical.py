import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from technical_analyzer import TechnicalAnalyzer

class TestTechnicalAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        dates = pd.date_range(start='2023-01-01', end='2023-03-01', freq='D')
        np.random.seed(42)
        
        self.sample_data = pd.DataFrame({
            'Open': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5),
            'High': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5) + np.random.rand(len(dates)),
            'Low': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5) - np.random.rand(len(dates)),
            'Close': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5),
            'Volume': np.random.randint(1000000, 5000000, len(dates))
        }, index=dates)
        
        self.analyzer = TechnicalAnalyzer(self.sample_data)
    
    def test_data_validation(self):
        """Test data validation"""
        self.assertTrue(self.analyzer.validate_data())
    
    def test_moving_averages(self):
        """Test moving average calculations"""
        result = self.analyzer.calculate_moving_averages()
        self.assertIn('SMA_20', result.columns)
        self.assertIn('EMA_12', result.columns)
        self.assertFalse(result['SMA_20'].isnull().all())
    
    def test_rsi_calculation(self):
        """Test RSI calculation"""
        result = self.analyzer.calculate_rsi()
        self.assertIn('RSI', result.columns)
        # RSI should be between 0 and 100
        self.assertTrue((result['RSI'].dropna() >= 0).all())
        self.assertTrue((result['RSI'].dropna() <= 100).all())
    
    def test_macd_calculation(self):
        """Test MACD calculation"""
        result = self.analyzer.calculate_macd()
        self.assertIn('MACD', result.columns)
        self.assertIn('MACD_Signal', result.columns)
        self.assertIn('MACD_Histogram', result.columns)
    
    def test_bollinger_bands(self):
        """Test Bollinger Bands calculation"""
        result = self.analyzer.calculate_bollinger_bands()
        self.assertIn('BB_Upper', result.columns)
        self.assertIn('BB_Lower', result.columns)
        # Upper band should be higher than lower band
        self.assertTrue((result['BB_Upper'] > result['BB_Lower']).all())
    
    def test_all_indicators(self):
        """Test calculation of all indicators"""
        result = self.analyzer.calculate_all_indicators()
        expected_indicators = ['SMA_20', 'RSI', 'MACD', 'BB_Upper', 'Stoch_K']
        for indicator in expected_indicators:
            self.assertIn(indicator, result.columns)
    
    def test_signal_generation(self):
        """Test trading signal generation"""
        self.analyzer.calculate_all_indicators()
        signals = self.analyzer.get_signals()
        self.assertIn('RSI_Overbought', signals.columns)
        self.assertIn('MACD_Bullish', signals.columns)

if __name__ == '__main__':
    unittest.main()