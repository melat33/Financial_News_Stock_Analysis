import pandas as pd
import numpy as np
import talib
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

class TechnicalAnalyzer:
    """
    Technical Analysis using TA-Lib for financial indicators
    """
    
    def __init__(self):
        self.indicators = {}
        
    def load_price_data(self, filepath: str) -> pd.DataFrame:
        """
        Load stock price data from CSV file
        Expected columns: Date, Open, High, Low, Close, Volume, Stock
        """
        try:
            df = pd.read_csv(filepath, parse_dates=['Date'])
            df = df.sort_values('Date')
            df.set_index('Date', inplace=True)
            print(f"✅ Loaded {len(df)} price records")
            return df
        except Exception as e:
            print(f"❌ Error loading price data: {e}")
            return pd.DataFrame()
    
    def calculate_moving_averages(self, df: pd.DataFrame, periods: List[int] = [20, 50, 200]) -> pd.DataFrame:
        """Calculate Simple Moving Averages"""
        for period in periods:
            df[f'SMA_{period}'] = talib.SMA(df['Close'], timeperiod=period)
        return df
    
    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Calculate Relative Strength Index"""
        df['RSI'] = talib.RSI(df['Close'], timeperiod=period)
        return df
    
    def calculate_macd(self, df: pd.DataFrame, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9) -> pd.DataFrame:
        """Calculate MACD indicator"""
        macd, macd_signal, macd_hist = talib.MACD(df['Close'], 
                                                 fastperiod=fastperiod, 
                                                 slowperiod=slowperiod, 
                                                 signalperiod=signalperiod)
        df['MACD'] = macd
        df['MACD_Signal'] = macd_signal
        df['MACD_Histogram'] = macd_hist
        return df
    
    def calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20, nbdev: int = 2) -> pd.DataFrame:
        """Calculate Bollinger Bands"""
        upper, middle, lower = talib.BBANDS(df['Close'], 
                                          timeperiod=period, 
                                          nbdevup=nbdev, 
                                          nbdevdn=nbdev)
        df['BB_Upper'] = upper
        df['BB_Middle'] = middle
        df['BB_Lower'] = lower
        df['BB_Width'] = (upper - lower) / middle  # Bollinger Band Width
        return df
    
    def calculate_stochastic(self, df: pd.DataFrame, fastk_period: int = 14, slowk_period: int = 3, slowd_period: int = 3) -> pd.DataFrame:
        """Calculate Stochastic Oscillator"""
        slowk, slowd = talib.STOCH(df['High'], df['Low'], df['Close'],
                                 fastk_period=fastk_period,
                                 slowk_period=slowk_period,
                                 slowd_period=slowd_period)
        df['Stoch_K'] = slowk
        df['Stoch_D'] = slowd
        return df
    
    def calculate_volume_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate volume-based indicators"""
        # On Balance Volume
        df['OBV'] = talib.OBV(df['Close'], df['Volume'])
        
        # Volume SMA
        df['Volume_SMA_20'] = talib.SMA(df['Volume'], timeperiod=20)
        
        return df
    
    def calculate_support_resistance(self, df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """
        Calculate support and resistance levels using recent highs and lows
        """
        df['Resistance'] = df['High'].rolling(window=window).max()
        df['Support'] = df['Low'].rolling(window=window).min()
        return df
    
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on technical indicators
        """
        # RSI signals
        df['RSI_Signal'] = 0
        df.loc[df['RSI'] < 30, 'RSI_Signal'] = 1  # Oversold - Buy
        df.loc[df['RSI'] > 70, 'RSI_Signal'] = -1  # Overbought - Sell
        
        # MACD signals
        df['MACD_Signal'] = 0
        df.loc[df['MACD'] > df['MACD_Signal'], 'MACD_Signal'] = 1
        df.loc[df['MACD'] < df['MACD_Signal'], 'MACD_Signal'] = -1
        
        # Bollinger Bands signals
        df['BB_Signal'] = 0
        df.loc[df['Close'] < df['BB_Lower'], 'BB_Signal'] = 1  # Below lower band - Buy
        df.loc[df['Close'] > df['BB_Upper'], 'BB_Signal'] = -1  # Above upper band - Sell
        
        # Combined signal
        df['Combined_Signal'] = df[['RSI_Signal', 'MACD_Signal', 'BB_Signal']].mean(axis=1)
        
        return df
    
    def calculate_performance_metrics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate performance metrics for the technical analysis
        """
        if len(df) == 0:
            return {}
            
        returns = df['Close'].pct_change().dropna()
        
        metrics = {
            'total_return': (df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100,
            'volatility': returns.std() * np.sqrt(252) * 100,  # Annualized
            'sharpe_ratio': returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0,
            'max_drawdown': (df['Close'] / df['Close'].cummax() - 1).min() * 100,
            'avg_volume': df['Volume'].mean(),
            'rsi_oversold_days': (df['RSI'] < 30).sum(),
            'rsi_overbought_days': (df['RSI'] > 70).sum()
        }
        
        return metrics
    
    def analyze_stock(self, filepath: str) -> pd.DataFrame:
        """
        Complete technical analysis for a stock
        """
        print(f"🔧 Performing technical analysis for {filepath}")
        
        # Load data
        df = self.load_price_data(filepath)
        if df.empty:
            return df
        
        # Calculate all indicators
        df = self.calculate_moving_averages(df)
        df = self.calculate_rsi(df)
        df = self.calculate_macd(df)
        df = self.calculate_bollinger_bands(df)
        df = self.calculate_stochastic(df)
        df = self.calculate_volume_indicators(df)
        df = self.calculate_support_resistance(df)
        df = self.generate_signals(df)
        
        print("✅ Technical analysis completed")
        return df