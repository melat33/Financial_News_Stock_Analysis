# src/feature_builder.py - Feature engineering for ML
import pandas as pd
import numpy as np
from src.config import TECHNICAL_INDICATORS

class FeatureBuilder:
    """Build features for machine learning models"""
    
    def calculate_technical_indicators(self, price_data):
        """Calculate technical indicators for stock data"""
        print("🔧 Calculating technical indicators...")
        
        features_data = []
        
        for ticker in price_data['ticker'].unique():
            ticker_data = price_data[price_data['ticker'] == ticker].copy()
            ticker_data = ticker_data.sort_values('date')
            
            # Simple Moving Averages
            ticker_data['SMA_20'] = ticker_data['Close'].rolling(window=20).mean()
            ticker_data['SMA_50'] = ticker_data['Close'].rolling(window=50).mean()
            
            # RSI (Relative Strength Index)
            ticker_data['RSI'] = self._calculate_rsi(ticker_data['Close'])
            
            # MACD
            ticker_data = self._calculate_macd(ticker_data)
            
            # Bollinger Bands
            ticker_data = self._calculate_bollinger_bands(ticker_data)
            
            features_data.append(ticker_data)
        
        if features_data:
            combined_features = pd.concat(features_data, ignore_index=True)
            print(f"✅ Technical indicators calculated for {len(features_data)} tickers")
            return combined_features
        else:
            return price_data
    
    def _calculate_rsi(self, prices, window=14):
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, df):
        """Calculate MACD indicator"""
        exp1 = df['Close'].ewm(span=12).mean()
        exp2 = df['Close'].ewm(span=26).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_histogram'] = df['MACD'] - df['MACD_signal']
        return df
    
    def _calculate_bollinger_bands(self, df, window=20):
        """Calculate Bollinger Bands"""
        df['BB_middle'] = df['Close'].rolling(window=window).mean()
        bb_std = df['Close'].rolling(window=window).std()
        df['BB_upper'] = df['BB_middle'] + (bb_std * 2)
        df['BB_lower'] = df['BB_middle'] - (bb_std * 2)
        df['BB_width'] = df['BB_upper'] - df['BB_lower']
        return df

# Singleton instance
feature_builder = FeatureBuilder()