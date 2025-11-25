import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score
import logging

class CorrelationAnalyzer:
    """
    Analyze correlation between news sentiment and stock movements
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def calculate_correlation_metrics(self, df, sentiment_col='combined_sentiment', return_col='daily_return'):
        """
        Calculate comprehensive correlation metrics
        """
        # Remove NaN values for correlation calculation
        clean_df = df[[sentiment_col, return_col]].dropna()
        
        if len(clean_df) < 2:
            self.logger.warning("Insufficient data for correlation analysis")
            return None
        
        sentiment_series = clean_df[sentiment_col]
        return_series = clean_df[return_col]
        
        # Calculate different correlation coefficients
        pearson_corr, pearson_p = pearsonr(sentiment_series, return_series)
        spearman_corr, spearman_p = spearmanr(sentiment_series, return_series)
        
        # R-squared
        r_squared = r2_score(return_series, sentiment_series)
        
        # Lagged correlations (1-day lag)
        if len(sentiment_series) > 1:
            lagged_corr, lagged_p = pearsonr(sentiment_series.iloc[:-1], return_series.iloc[1:])
        else:
            lagged_corr = lagged_p = np.nan
        
        metrics = {
            'pearson_correlation': pearson_corr,
            'pearson_p_value': pearson_p,
            'spearman_correlation': spearman_corr,
            'spearman_p_value': spearman_p,
            'r_squared': r_squared,
            'lagged_correlation': lagged_corr,
            'lagged_p_value': lagged_p,
            'n_observations': len(clean_df),
            'correlation_strength': self._interpret_correlation_strength(pearson_corr)
        }
        
        self.logger.info(f"Correlation Analysis Results:")
        self.logger.info(f"Pearson Correlation: {pearson_corr:.4f} (p-value: {pearson_p:.4f})")
        self.logger.info(f"Correlation Strength: {metrics['correlation_strength']}")
        
        return metrics
    
    def _interpret_correlation_strength(self, correlation):
        """Interpret correlation coefficient strength"""
        abs_corr = abs(correlation)
        if abs_corr >= 0.7:
            return "Very Strong"
        elif abs_corr >= 0.5:
            return "Strong"
        elif abs_corr >= 0.3:
            return "Moderate"
        elif abs_corr >= 0.1:
            return "Weak"
        else:
            return "Very Weak"
    
    def sentiment_impact_analysis(self, df, sentiment_col='sentiment_category', return_col='daily_return'):
        """Analyze returns by sentiment category"""
        category_returns = df.groupby(sentiment_col)[return_col].agg([
            'count', 'mean', 'std', 'min', 'max', 'median'
        ]).round(4)
        
        # Calculate percentage of positive returns by category
        positive_returns_pct = df.groupby(sentiment_col)[return_col].apply(
            lambda x: (x > 0).sum() / len(x) * 100
        ).round(2)
        
        category_returns['positive_returns_pct'] = positive_returns_pct
        
        return category_returns
    
    def create_correlation_report(self, df, sentiment_cols=None):
        """Generate comprehensive correlation report"""
        if sentiment_cols is None:
            sentiment_cols = ['textblob_sentiment', 'vader_sentiment', 'combined_sentiment']
        
        report = {}
        
        for sentiment_col in sentiment_cols:
            if sentiment_col in df.columns:
                metrics = self.calculate_correlation_metrics(df, sentiment_col)
                if metrics:
                    report[sentiment_col] = metrics
        
        return report

# Singleton instance
correlation_analyzer = CorrelationAnalyzer()