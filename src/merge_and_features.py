import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.config import PROCESSED_DIR

class DataMerger:
    """
    Handle date alignment and merging of news sentiment with stock data
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def normalize_dates(self, df, date_column='date'):
        """Normalize dates to ensure proper alignment - FIXED for timezone issues"""
        df_normalized = df.copy()
        
        # Convert to datetime with proper timezone handling
        df_normalized[date_column] = pd.to_datetime(df_normalized[date_column], errors='coerce', utc=True)
        
        # Remove timezone info and normalize to date only
        df_normalized[date_column] = df_normalized[date_column].dt.tz_convert(None).dt.normalize()
        
        # Remove any rows with invalid dates
        df_normalized = df_normalized.dropna(subset=[date_column])
        
        return df_normalized
    
    def align_with_trading_days(self, news_df, stock_df, news_date_col='date', stock_date_col='date'):
        """
        Align news dates with stock trading days
        Handles cases where news might be published on non-trading days
        """
        # Normalize dates
        news_normalized = self.normalize_dates(news_df, news_date_col)
        stock_normalized = self.normalize_dates(stock_df, stock_date_col)
        
        # Get all trading days
        trading_days = set(stock_normalized[stock_date_col].dt.date)
        
        def map_to_trading_day(date):
            """Map news date to nearest trading day"""
            try:
                date = date.date()
                
                # If news is on trading day, use it directly
                if date in trading_days:
                    return date
                
                # Otherwise find next trading day
                next_day = date + timedelta(days=1)
                while next_day not in trading_days and (next_day - date).days < 7:  # Look max 7 days ahead
                    next_day += timedelta(days=1)
                
                if next_day in trading_days:
                    return next_day
                
                # If no future trading day found, use previous trading day
                prev_day = date - timedelta(days=1)
                while prev_day not in trading_days and (date - prev_day).days < 7:
                    prev_day -= timedelta(days=1)
                
                return prev_day if prev_day in trading_days else date
            except Exception as e:
                self.logger.warning(f"Error mapping date {date}: {e}")
                return date
        
        # Apply mapping
        news_normalized['aligned_date'] = news_normalized[news_date_col].apply(map_to_trading_day)
        news_normalized['aligned_date'] = pd.to_datetime(news_normalized['aligned_date'])
        
        return news_normalized, stock_normalized
    
    def calculate_daily_returns(self, stock_df, price_column='close', date_column='date'):
        """Calculate daily percentage returns"""
        try:
            stock_df = stock_df.sort_values(date_column).copy()
            stock_df['daily_return'] = stock_df[price_column].pct_change() * 100
            stock_df['daily_return'] = stock_df['daily_return'].replace([np.inf, -np.inf], np.nan)
            
            return stock_df
        except Exception as e:
            self.logger.error(f"Error calculating daily returns: {e}")
            return stock_df
    
    def merge_sentiment_returns(self, sentiment_df, stock_df, 
                               sentiment_date_col='aligned_date', 
                               stock_date_col='date',
                               news_ticker_col='stock',
                               stock_ticker_col='ticker'):
        """
        Merge sentiment data with stock returns for multiple companies
        """
        print("🔄 Merging sentiment with stock returns...")
        
        try:
            # Aggregate daily sentiment by date AND company
            daily_sentiment = sentiment_df.groupby([sentiment_date_col, news_ticker_col]).agg({
                'textblob_sentiment': 'mean',
                'vader_sentiment': 'mean', 
                'combined_sentiment': 'mean',
                'sentiment_category': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'neutral'
            }).reset_index()
            
            daily_sentiment = daily_sentiment.rename(columns={
                sentiment_date_col: 'date',
                news_ticker_col: 'ticker'
            })
            
            print(f"📊 Daily sentiment by company: {len(daily_sentiment)} records")
            print(f"🏢 Companies in sentiment: {sorted(daily_sentiment['ticker'].unique())}")
            print(f"🏢 Companies in stock data: {sorted(stock_df[stock_ticker_col].unique())}")
            
            # Merge with stock data on both date AND ticker
            merged_data = pd.merge(
                stock_df, 
                daily_sentiment, 
                on=['date', 'ticker'], 
                how='inner'
            )
            
            self.logger.info(f"✅ Merged dataset shape: {merged_data.shape}")
            self.logger.info(f"📅 Date range: {merged_data['date'].min()} to {merged_data['date'].max()}")
            self.logger.info(f"🏢 Companies in merged data: {sorted(merged_data['ticker'].unique())}")
            print("📈 Records per company:")
            print(merged_data['ticker'].value_counts())
            
            return merged_data
            
        except Exception as e:
            self.logger.error(f"Error merging sentiment with returns: {e}")
            # Return empty dataframe with expected columns
            return pd.DataFrame(columns=['date', 'ticker', 'close', 'daily_return', 'textblob_sentiment', 
                                       'vader_sentiment', 'combined_sentiment', 'sentiment_category'])

# Singleton instance
data_merger = DataMerger()