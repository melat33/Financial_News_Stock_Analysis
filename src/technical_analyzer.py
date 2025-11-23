import pandas as pd
import numpy as np
import talib
from pynance import technical
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Dict, List
import warnings
warnings.filterwarnings('ignore')

class TechnicalAnalyzer:
    """
    Technical Analysis using TA-Lib and PyNance for financial data
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with financial data
        
        Args:
            data: DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Volume']
        """
        self.data = data.copy()
        self.indicators = {}
        
    def validate_data(self) -> bool:
        """Validate if required columns are present"""
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        return all(col in self.data.columns for col in required_cols)
    
    def calculate_moving_averages(self, windows: List[int] = [5, 10, 20, 50]) -> pd.DataFrame:
        """Calculate various moving averages"""
        if not self.validate_data():
            raise ValueError("Missing required columns in data")
            
        close_prices = self.data['Close']
        
        for window in windows:
            self.data[f'SMA_{window}'] = talib.SMA(close_prices, timeperiod=window)
            self.data[f'EMA_{window}'] = talib.EMA(close_prices, timeperiod=window)
            
        self.indicators['moving_averages'] = [f'SMA_{w}' for w in windows] + [f'EMA_{w}' for w in windows]
        return self.data
    
    def calculate_rsi(self, period: int = 14) -> pd.DataFrame:
        """Calculate Relative Strength Index"""
        self.data['RSI'] = talib.RSI(self.data['Close'], timeperiod=period)
        self.indicators['rsi'] = ['RSI']
        return self.data
    
    def calculate_macd(self, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9) -> pd.DataFrame:
        """Calculate MACD indicator"""
        macd, macd_signal, macd_hist = talib.MACD(
            self.data['Close'], 
            fastperiod=fastperiod, 
            slowperiod=slowperiod, 
            signalperiod=signalperiod
        )
        
        self.data['MACD'] = macd
        self.data['MACD_Signal'] = macd_signal
        self.data['MACD_Histogram'] = macd_hist
        
        self.indicators['macd'] = ['MACD', 'MACD_Signal', 'MACD_Histogram']
        return self.data
    
    def calculate_bollinger_bands(self, period: int = 20, nbdev: int = 2) -> pd.DataFrame:
        """Calculate Bollinger Bands"""
        upper, middle, lower = talib.BBANDS(
            self.data['Close'], 
            timeperiod=period, 
            nbdevup=nbdev, 
            nbdevdn=nbdev
        )
        
        self.data['BB_Upper'] = upper
        self.data['BB_Middle'] = middle
        self.data['BB_Lower'] = lower
        self.data['BB_Width'] = (upper - lower) / middle  # Bollinger Band Width
        
        self.indicators['bollinger_bands'] = ['BB_Upper', 'BB_Middle', 'BB_Lower', 'BB_Width']
        return self.data
    
    def calculate_stochastic(self, fastk_period: int = 14, slowk_period: int = 3, slowd_period: int = 3) -> pd.DataFrame:
        """Calculate Stochastic Oscillator"""
        slowk, slowd = talib.STOCH(
            self.data['High'], 
            self.data['Low'], 
            self.data['Close'],
            fastk_period=fastk_period,
            slowk_period=slowk_period,
            slowk_matype=0,
            slowd_period=slowd_period,
            slowd_matype=0
        )
        
        self.data['Stoch_K'] = slowk
        self.data['Stoch_D'] = slowd
        
        self.indicators['stochastic'] = ['Stoch_K', 'Stoch_D']
        return self.data
    
    def calculate_volume_indicators(self) -> pd.DataFrame:
        """Calculate volume-based indicators"""
        # Volume SMA
        self.data['Volume_SMA_20'] = talib.SMA(self.data['Volume'], timeperiod=20)
        
        # On Balance Volume (OBV)
        self.data['OBV'] = talib.OBV(self.data['Close'], self.data['Volume'])
        
        self.indicators['volume'] = ['Volume_SMA_20', 'OBV']
        return self.data
    
    def calculate_support_resistance(self, window: int = 20) -> pd.DataFrame:
        """Calculate support and resistance levels"""
        self.data['Resistance'] = self.data['High'].rolling(window=window).max()
        self.data['Support'] = self.data['Low'].rolling(window=window).min()
        
        self.indicators['support_resistance'] = ['Resistance', 'Support']
        return self.data
    
    def calculate_all_indicators(self) -> pd.DataFrame:
        """Calculate all technical indicators"""
        print("Calculating all technical indicators...")
        
        self.calculate_moving_averages()
        self.calculate_rsi()
        self.calculate_macd()
        self.calculate_bollinger_bands()
        self.calculate_stochastic()
        self.calculate_volume_indicators()
        self.calculate_support_resistance()
        
        print("All technical indicators calculated successfully!")
        return self.data
    
    def get_signals(self) -> pd.DataFrame:
        """Generate trading signals based on indicators"""
        signals = self.data.copy()
        
        # RSI signals
        signals['RSI_Overbought'] = signals['RSI'] > 70
        signals['RSI_Oversold'] = signals['RSI'] < 30
        
        # MACD signals
        signals['MACD_Bullish'] = signals['MACD'] > signals['MACD_Signal']
        signals['MACD_Bearish'] = signals['MACD'] < signals['MACD_Signal']
        
        # Bollinger Bands signals
        signals['BB_Upper_Break'] = signals['Close'] > signals['BB_Upper']
        signals['BB_Lower_Break'] = signals['Close'] < signals['BB_Lower']
        
        # Stochastic signals
        signals['Stoch_Overbought'] = signals['Stoch_K'] > 80
        signals['Stoch_Oversold'] = signals['Stoch_K'] < 20
        
        return signals

def load_sample_data() -> pd.DataFrame:
    """Load sample financial data for testing"""
    # Generate sample data
    dates = pd.date_range(start='2020-01-01', end='2024-01-01', freq='D')
    np.random.seed(42)
    
    data = pd.DataFrame({
        'Date': dates,
        'Open': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5),
        'High': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5) + np.random.rand(len(dates)),
        'Low': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5) - np.random.rand(len(dates)),
        'Close': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5),
        'Volume': np.random.randint(1000000, 5000000, len(dates))
    })
    
    data.set_index('Date', inplace=True)
    return data

if __name__ == "__main__":
    # Example usage
    sample_data = load_sample_data()
    analyzer = TechnicalAnalyzer(sample_data)
    analyzed_data = analyzer.calculate_all_indicators()
    print("Technical analysis completed!")
    print(f"Available indicators: {analyzer.indicators.keys()}")