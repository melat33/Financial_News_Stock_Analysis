#!/usr/bin/env python3
"""
Task 1 - News Analysis EDA (Fixed - No src dependencies)
Exploratory Data Analysis for financial news data
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

print(f"📁 Project root: {project_root}")

# Configuration
TICKERS = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'NVDA']
NEWS_FILE = os.path.join(project_root, 'data', 'raw', 'financial_news.csv')
REPORTS_DIR = os.path.join(project_root, 'reports')
PLOTS_DIR = os.path.join(REPORTS_DIR, 'plots')

# Create directories
for directory in [REPORTS_DIR, PLOTS_DIR]:
    os.makedirs(directory, exist_ok=True)

def load_news_data():
    """Load news data without dependencies"""
    print("📰 Loading news data...")
    
    if not os.path.exists(NEWS_FILE):
        print(f"❌ News file not found: {NEWS_FILE}")
        print("💡 Please run: python scripts/download_news_data.py first")
        return None
    
    try:
        df = pd.read_csv(NEWS_FILE)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
        
        print(f"✅ News data loaded: {len(df)} articles")
        return df
    except Exception as e:
        print(f"❌ Error loading news data: {e}")
        return None

def setup_plotting():
    """Setup matplotlib and seaborn styles"""
    plt.style.use('default')
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (12, 8)
    print("✅ Plotting setup complete")

def perform_basic_analysis(df):
    """Perform basic data analysis"""
    print("\n🔍 BASIC DATA ANALYSIS")
    print("=" * 50)
    
    print(f"📊 Total Articles: {len(df):,}")
    print(f"📅 Date Range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
    print(f"🏢 Companies: {df['stock'].nunique()}")
    print(f"📰 Publishers: {df['publisher'].nunique() if 'publisher' in df.columns else 'N/A'}")
    
    # Missing values
    missing = df.isnull().sum()
    if missing.any():
        print(f"⚠️  Missing values: {missing.sum()} total")
        for col, count in missing[missing > 0].items():
            print(f"   • {col}: {count} missing")
    
    return df

def analyze_companies(df):
    """Analyze news distribution by company"""
    print("\n🏢 COMPANY ANALYSIS")
    print("=" * 50)
    
    company_counts = df['stock'].value_counts()
    
    print("📈 Articles per Company:")
    for company, count in company_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   • {company}: {count} articles ({percentage:.1f}%)")
    
    return company_counts

def analyze_temporal_patterns(df):
    """Analyze time-based patterns"""
    print("\n📅 TEMPORAL ANALYSIS")
    print("=" * 50)
    
    df['date_only'] = df['date'].dt.date
    daily_counts = df['date_only'].value_counts().sort_index()
    
    print(f"📆 Total Days: {daily_counts.shape[0]}")
    print(f"📈 Avg Articles per Day: {len(df)/daily_counts.shape[0]:.1f}")
    print(f"🔥 Most Active Day: {daily_counts.index[0]} with {daily_counts.iloc[0]} articles")
    print(f"😴 Least Active Day: {daily_counts.index[-1]} with {daily_counts.iloc[-1]} articles")
    
    return daily_counts

def analyze_text_features(df):
    """Analyze text-based features"""
    print("\n🔤 TEXT ANALYSIS")
    print("=" * 50)
    
    df['headline_length'] = df['headline'].str.len()
    df['word_count'] = df['headline'].str.split().str.len()
    
    print(f"📝 Headline Length:")
    print(f"   • Average: {df['headline_length'].mean():.1f} characters")
    print(f"   • Longest: {df['headline_length'].max()} characters")
    print(f"   • Shortest: {df['headline_length'].min()} characters")
    
    print(f"📊 Word Count:")
    print(f"   • Average: {df['word_count'].mean():.1f} words")
    print(f"   • Most: {df['word_count'].max()} words")
    print(f"   • Fewest: {df['word_count'].min()} words")
    
    return df

def analyze_sentiment(df):
    """Analyze sentiment distribution"""
    if 'sentiment' not in df.columns:
        print("❌ Sentiment data not available")
        return None
    
    print("\n😊 SENTIMENT ANALYSIS")
    print("=" * 50)
    
    sentiment_counts = df['sentiment'].value_counts()
    
    print("🎭 Sentiment Distribution:")
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   • {sentiment.capitalize()}: {count} articles ({percentage:.1f}%)")
    
    # Sentiment by company
    print("\n🏢 Sentiment by Company:")
    sentiment_by_company = pd.crosstab(df['stock'], df['sentiment'])
    for company in df['stock'].unique():
        company_data = df[df['stock'] == company]
        if len(company_data) > 0:
            sentiment_dist = company_data['sentiment'].value_counts()
            print(f"   • {company}: {sentiment_dist.to_dict()}")
    
    return sentiment_counts

def create_visualizations(df):
    """Create comprehensive visualizations"""
    print("\n📈 CREATING VISUALIZATIONS...")
    
    try:
        # Create a 2x2 grid of plots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Financial News Data Analysis - Task 1', fontsize=16, fontweight='bold')
        
        # 1. Company Distribution
        company_counts = df['stock'].value_counts()
        axes[0, 0].bar(company_counts.index, company_counts.values, color='skyblue', alpha=0.7)
        axes[0, 0].set_title('Articles by Company')
        axes[0, 0].set_xlabel('Company')
        axes[0, 0].set_ylabel('Number of Articles')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for i, v in enumerate(company_counts.values):
            axes[0, 0].text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')
        
        # 2. Sentiment Distribution (if available)
        if 'sentiment' in df.columns:
            sentiment_counts = df['sentiment'].value_counts()
            colors = ['green', 'gray', 'red']  # positive, neutral, negative
            axes[0, 1].pie(sentiment_counts.values, labels=sentiment_counts.index, 
                          autopct='%1.1f%%', colors=colors[:len(sentiment_counts)], startangle=90)
            axes[0, 1].set_title('Sentiment Distribution')
        else:
            # Word count distribution as fallback
            axes[0, 1].hist(df['word_count'], bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
            axes[0, 1].set_title('Headline Word Count Distribution')
            axes[0, 1].set_xlabel('Words per Headline')
            axes[0, 1].set_ylabel('Frequency')
        
        # 3. Headline Length Distribution
        axes[1, 0].hist(df['headline_length'], bins=30, alpha=0.7, color='orange', edgecolor='black')
        axes[1, 0].axvline(df['headline_length'].mean(), color='red', linestyle='--', 
                          label=f'Mean: {df["headline_length"].mean():.1f}')
        axes[1, 0].set_title('Headline Length Distribution')
        axes[1, 0].set_xlabel('Headline Length (characters)')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].legend()
        
        # 4. Timeline (last 30 days)
        df['date_only'] = df['date'].dt.date
        last_30_days = df[df['date'] >= (df['date'].max() - pd.Timedelta(days=30))]
        daily_counts = last_30_days['date_only'].value_counts().sort_index()
        
        axes[1, 1].plot(daily_counts.index, daily_counts.values, marker='o', linewidth=2, color='purple')
        axes[1, 1].set_title('Articles Published (Last 30 Days)')
        axes[1, 1].set_xlabel('Date')
        axes[1, 1].set_ylabel('Articles per Day')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Save the plot
        plot_file = os.path.join(PLOTS_DIR, 'task1_news_analysis.png')
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        print(f"✅ Visualizations saved to: {plot_file}")
        
        plt.show()
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")
        # Create a simple fallback plot
        plt.figure(figsize=(10, 6))
        company_counts = df['stock'].value_counts()
        plt.bar(company_counts.index, company_counts.values)
        plt.title('Articles by Company')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'fallback_analysis.png'), dpi=300, bbox_inches='tight')
        plt.show()

def generate_summary_report(df):
    """Generate a comprehensive summary report"""
    print("\n📋 GENERATING SUMMARY REPORT...")
    
    # Create summary statistics
    summary = {
        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_articles': len(df),
        'date_range_start': df['date'].min().strftime('%Y-%m-%d'),
        'date_range_end': df['date'].max().strftime('%Y-%m-%d'),
        'companies_covered': df['stock'].nunique(),
        'companies_list': ', '.join(sorted(df['stock'].unique())),
        'publishers_count': df['publisher'].nunique() if 'publisher' in df.columns else 0,
        'avg_headline_length': round(df['headline_length'].mean(), 1),
        'avg_word_count': round(df['word_count'].mean(), 1),
        'data_quality_score': f"{(1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100:.1f}%"
    }
    
    # Add sentiment info if available
    if 'sentiment' in df.columns:
        sentiment_dist = df['sentiment'].value_counts()
        summary['sentiment_positive'] = sentiment_dist.get('positive', 0)
        summary['sentiment_neutral'] = sentiment_dist.get('neutral', 0)
        summary['sentiment_negative'] = sentiment_dist.get('negative', 0)
    
    # Save summary to CSV
    summary_df = pd.DataFrame([summary])
    summary_file = os.path.join(REPORTS_DIR, 'task1_eda_summary.csv')
    summary_df.to_csv(summary_file, index=False)
    print(f"✅ Summary report saved to: {summary_file}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TASK 1 - EDA SUMMARY REPORT")
    print("=" * 60)
    for key, value in summary.items():
        formatted_key = key.replace('_', ' ').title()
        print(f"   • {formatted_key}: {value}")
    print("=" * 60)

def main():
    """Main function"""
    print("🚀 TASK 1 - NEWS EXPLORATORY DATA ANALYSIS")
    print("=" * 60)
    
    # Setup
    setup_plotting()
    
    # Load data
    df = load_news_data()
    if df is None:
        return
    
    # Perform analyses
    df = perform_basic_analysis(df)
    company_analysis = analyze_companies(df)
    temporal_analysis = analyze_temporal_patterns(df)
    df = analyze_text_features(df)
    sentiment_analysis = analyze_sentiment(df)
    
    # Create visualizations
    create_visualizations(df)
    
    # Generate summary report
    generate_summary_report(df)
    
    print("\n✅ TASK 1 - EDA COMPLETED SUCCESSFULLY!")
    print("\n🎯 NEXT STEPS FOR NEWS ANALYSIS:")
    print("   1. Review the EDA summary in reports/task1_eda_summary.csv")
    print("   2. Check visualizations in reports/plots/task1_news_analysis.png")
    print("   3. Proceed with advanced sentiment analysis")
    print("   4. Build news trend dashboards")
    print("   5. Analyze sentiment impact on stock prices")

if __name__ == "__main__":
    main()