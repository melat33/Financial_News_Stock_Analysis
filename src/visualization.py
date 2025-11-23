from typing import Dict, List, Optional  # ← ADD THIS IMPORT
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

class FinancialVisualizer:
    def __init__(self, style: str = 'seaborn-v0_8', figsize: tuple = (15, 8)):
        self.style = style
        self.figsize = figsize
        plt.style.use(self.style)
        
        # Color scheme for different stocks
        self.colors = {
            'AAPL': '#A2AAAD', 'AMZN': '#FF9900', 'GOOG': '#4285F4',
            'META': '#1877F2', 'MSFT': '#737373', 'NVDA': '#76B900'
        }
    
    def set_style(self, style: str):
        """Set the matplotlib style"""
        plt.style.use(style)
        self.style = style
    
    def create_price_chart(self, data: pd.DataFrame, ticker: str, 
                         save_path: Optional[str] = None) -> plt.Figure:
        """Create a price chart with moving averages"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize, 
                                      gridspec_kw={'height_ratios': [3, 1]})
        
        # Price data
        price_data = data[data['Stock'] == ticker].copy()
        price_data = price_data.sort_values('Date')
        
        # Plot prices and moving averages
        ax1.plot(price_data['Date'], price_data['Close'], 
                label='Close Price', color=self.colors.get(ticker, '#1f77b4'), linewidth=2)
        
        # Plot moving averages if they exist
        ma_columns = [col for col in price_data.columns if 'MA' in col]
        for ma in ma_columns[:3]:  # Plot first 3 MAs
            ax1.plot(price_data['Date'], price_data[ma], 
                    label=ma, alpha=0.7, linestyle='--')
        
        ax1.set_title(f'{ticker} - Price Chart with Moving Averages', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Price ($)', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot volume
        ax2.bar(price_data['Date'], price_data['Volume'], 
               color=self.colors.get(ticker, '#1f77b4'), alpha=0.7)
        ax2.set_title('Volume', fontsize=12)
        ax2.set_ylabel('Volume', fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Chart saved: {save_path}")
        
        return fig
    
    def create_technical_indicators_chart(self, data: pd.DataFrame, ticker: str,
                                        save_path: Optional[str] = None) -> plt.Figure:
        """Create a comprehensive technical indicators chart"""
        tech_data = data[data['Stock'] == ticker].copy()
        tech_data = tech_data.sort_values('Date')
        
        fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        
        # 1. Price with Bollinger Bands
        if all(col in tech_data.columns for col in ['Close', 'BB_upper', 'BB_lower']):
            axes[0].plot(tech_data['Date'], tech_data['Close'], label='Close Price', 
                        color=self.colors.get(ticker, '#1f77b4'), linewidth=2)
            axes[0].plot(tech_data['Date'], tech_data['BB_upper'], 
                        label='Bollinger Upper', color='red', alpha=0.7)
            axes[0].plot(tech_data['Date'], tech_data['BB_lower'], 
                        label='Bollinger Lower', color='green', alpha=0.7)
            axes[0].fill_between(tech_data['Date'], tech_data['BB_upper'], 
                               tech_data['BB_lower'], alpha=0.2)
            axes[0].set_title(f'{ticker} - Bollinger Bands', fontweight='bold')
            axes[0].legend()
            axes[0].grid(True, alpha=0.3)
        
        # 2. RSI
        if 'RSI' in tech_data.columns:
            axes[1].plot(tech_data['Date'], tech_data['RSI'], 
                        color='purple', linewidth=2)
            axes[1].axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Overbought')
            axes[1].axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Oversold')
            axes[1].set_title('RSI (Relative Strength Index)')
            axes[1].set_ylim(0, 100)
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)
        
        # 3. MACD
        if all(col in tech_data.columns for col in ['MACD', 'MACD_signal']):
            axes[2].plot(tech_data['Date'], tech_data['MACD'], 
                        label='MACD', color='blue', linewidth=2)
            axes[2].plot(tech_data['Date'], tech_data['MACD_signal'], 
                        label='Signal Line', color='red', linewidth=2)
            axes[2].bar(tech_data['Date'], tech_data.get('MACD_hist', 0), 
                       label='Histogram', color='gray', alpha=0.5)
            axes[2].set_title('MACD')
            axes[2].legend()
            axes[2].grid(True, alpha=0.3)
        
        # 4. Stochastic
        if all(col in tech_data.columns for col in ['Stoch_K', 'Stoch_D']):
            axes[3].plot(tech_data['Date'], tech_data['Stoch_K'], 
                        label='%K', color='blue', linewidth=2)
            axes[3].plot(tech_data['Date'], tech_data['Stoch_D'], 
                        label='%D', color='red', linewidth=2)
            axes[3].axhline(y=80, color='r', linestyle='--', alpha=0.7, label='Overbought')
            axes[3].axhline(y=20, color='g', linestyle='--', alpha=0.7, label='Oversold')
            axes[3].set_title('Stochastic Oscillator')
            axes[3].legend()
            axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Technical chart saved: {save_path}")
        
        return fig

    def create_performance_dashboard(self, metrics_dict: Dict, title: str = "Performance Dashboard") -> plt.Figure:
        """Create a performance dashboard - FIXED TYPING"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.flatten()
        
        # Example implementation - customize based on your metrics
        if 'returns' in metrics_dict:
            axes[0].plot(metrics_dict['returns'], label='Returns')
            axes[0].set_title('Returns Over Time')
            axes[0].legend()
        
        if 'volatility' in metrics_dict:
            axes[1].bar(range(len(metrics_dict['volatility'])), metrics_dict['volatility'])
            axes[1].set_title('Volatility')
        
        # Add more plots based on your metrics
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig

    def create_correlation_heatmap(self, data: pd.DataFrame, 
                                 save_path: Optional[str] = None) -> plt.Figure:
        """Create correlation heatmap for multiple stocks"""
        # Pivot to get close prices by date and stock
        close_prices = data.pivot_table(index='Date', columns='Stock', values='Close')
        
        # Calculate correlations
        correlation_matrix = close_prices.corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, ax=ax, cbar_kws={'shrink': 0.8})
        
        ax.set_title('Stock Correlation Heatmap', fontsize=16, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Heatmap saved: {save_path}")
        
        return fig

# Alternative class name for compatibility
Visualization = FinancialVisualizer