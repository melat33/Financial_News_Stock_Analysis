import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append('../src')
from technical_analyzer import TechnicalAnalyzer

class TestTechnicalAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.analyzer = TechnicalAnalyzer()
        
        # Create sample price data
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        self.sample_data = pd.DataFrame({
            'Date': dates,
            'Open': np.random.normal(100, 10, 100).cumsum() + 100,
            'High': np.random.normal(105, 12, 100).cumsum() + 100,
            'Low': np.random.normal(95, 12, 100).cumsum() + 100,
            'Close': np.random.normal(100, 10, 100).cumsum() + 100,
            'Volume': np.random.randint(1000000, 50000000, 100),
            'Stock': 'TEST'
        })
        
        # Ensure High is highest, Low is lowest
        self.sample_data['High'] = self.sample_data[['Open', 'Close', 'High']].max(axis=1) + 2
        self.sample_data['Low'] = self.sample_data[['Open', 'Close', 'Low']].min(axis=1) - 2
        
        # Save test data
        os.makedirs('../data/prices', exist_ok=True)
        self.sample_data.to_csv('../data/prices/TEST_prices.csv', index=False)
    
    def test_load_price_data(self):
        """Test loading price data"""
        df = self.analyzer.load_price_data('../data/prices/TEST_prices.csv')
        self.assertFalse(df.empty)
        self.assertIn('Close', df.columns)
        self.assertIn('Volume', df.columns)
    
    def test_moving_averages(self):
        """Test moving average calculation"""
        df = self.analyzer.load_price_data('../data/prices/TEST_prices.csv')
        df = self.analyzer.calculate_moving_averages(df, [20, 50])
        
        self.assertIn('SMA_20', df.columns)
        self.assertIn('SMA_50', df.columns)
        self.assertFalse(df['SMA_20'].isna().all())
    
    def test_rsi_calculation(self):
        """Test RSI calculation"""
        df = self.analyzer.load_price_data('../data/prices/TEST_prices.csv')
        df = self.analyzer.calculate_rsi(df)
        
        self.assertIn('RSI', df.columns)
        # RSI should be between 0 and 100
        self.assertTrue((df['RSI'].dropna() <= 100).all())
        self.assertTrue((df['RSI'].dropna() >= 0).all())
    
    def test_macd_calculation(self):
        """Test MACD calculation"""
        df = self.analyzer.load_price_data('../data/prices/TEST_prices.csv')
        df = self.analyzer.calculate_macd(df)
        
        self.assertIn('MACD', df.columns)
        self.assertIn('MACD_Signal', df.columns)
        self.assertIn('MACD_Histogram', df.columns)
    
    def test_bollinger_bands(self):
        """Test Bollinger Bands calculation"""
        df = self.analyzer.load_price_data('../data/prices/TEST_prices.csv')
        df = self.analyzer.calculate_bollinger_bands(df)
        
        self.assertIn('BB_Upper', df.columns)
        self.assertIn('BB_Middle', df.columns)
        self.assertIn('BB_Lower', df.columns)
        # Upper band should be higher than lower band
        self.assertTrue((df['BB_Upper'] > df['BB_Lower']).all())
    
    def test_performance_metrics(self):
        """Test performance metrics calculation"""
        df = self.analyzer.load_price_data('../data/prices/TEST_prices.csv')
        metrics = self.analyzer.calculate_performance_metrics(df)
        
        self.assertIsInstance(metrics, dict)
        self.assertIn('total_return', metrics)
        self.assertIn('volatility', metrics)
        self.assertIn('sharpe_ratio', metrics)
    
    def test_signal_generation(self):
        """Test trading signal generation"""
        df = self.analyzer.load_price_data('../data/prices/TEST_prices.csv')
        df = self.analyzer.calculate_rsi(df)
        df = self.analyzer.calculate_macd(df)
        df = self.analyzer.calculate_bollinger_bands(df)
        df = self.analyzer.generate_signals(df)
        
        self.assertIn('RSI_Signal', df.columns)
        self.assertIn('MACD_Signal', df.columns)
        self.assertIn('BB_Signal', df.columns)
        self.assertIn('Combined_Signal', df.columns)

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)