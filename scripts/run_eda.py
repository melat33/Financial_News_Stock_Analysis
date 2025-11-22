import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_loader import load_news_data, validate_news_data
from src.text_analyzer import TextAnalyzer
from src.config import TICKERS

class EDAProcessor:
    def __init__(self):
        self.df = None
        self.text_analyzer = TextAnalyzer()
        plt.style.use('seaborn-v0_8')
        
    def load_and_validate(self):
        """Load and validate news data"""
        print("📥 LOADING NEWS DATA...")
        self.df = load_news_data()
        if self.df is not None:
            self.df = validate_news_data(self.df)
        return self.df is not None
    
    def run_descriptive_analysis(self):
        """Run comprehensive descriptive analysis"""
        print("\n" + "="*60)
        print("📊 DESCRIPTIVE STATISTICS ANALYSIS")
        print("="*60)
        
        # Basic statistics
        print(f"\n📈 BASIC STATISTICS:")
        print(f"   Total articles: {len(self.df):,}")
        print(f"   Date range: {self.df['date'].min()} to {self.df['date'].max()}")
        print(f"   Days covered: {(self.df['date'].max() - self.df['date'].min()).days} days")
        
        # Articles by company
        print(f"\n🏢 ARTICLES BY COMPANY:")
        company_counts = self.df['stock'].value_counts()
        for company, count in company_counts.items():
            print(f"   {company}: {count:,} articles ({count/len(self.df)*100:.1f}%)")
        
        # Text statistics
        print(f"\n🔤 TEXT STATISTICS:")
        print(f"   Avg headline length: {self.df['headline_length'].mean():.1f} chars")
        print(f"   Avg word count: {self.df['word_count'].mean():.1f} words")
        print(f"   Avg word length: {self.df['avg_word_length'].mean():.1f} chars")
        
        # Publisher analysis
        if 'publisher' in self.df.columns:
            print(f"\n📰 PUBLISHER ANALYSIS:")
            publisher_counts = self.df['publisher'].value_counts()
            print(f"   Total publishers: {len(publisher_counts)}")
            print(f"   Top 5 publishers:")
            for pub, count in publisher_counts.head(5).items():
                print(f"     {pub}: {count:,} articles")
    
    def run_time_series_analysis(self):
        """Analyze news frequency over time"""
        print("\n" + "="*60)
        print("⏰ TIME SERIES ANALYSIS")
        print("="*60)
        
        # Daily article count
        daily_counts = self.df.groupby(self.df['date'].dt.date).size()
        
        print(f"\n📅 DAILY FREQUENCY:")
        print(f"   Avg articles per day: {daily_counts.mean():.1f}")
        print(f"   Max articles in one day: {daily_counts.max()}")
        print(f"   Min articles in one day: {daily_counts.min()}")
        print(f"   Busiest day: {daily_counts.idxmax()} with {daily_counts.max()} articles")
        
        # Monthly trends
        monthly_counts = self.df.groupby(self.df['date'].dt.to_period('M')).size()
        print(f"\n📈 MONTHLY TRENDS:")
        print(f"   Avg articles per month: {monthly_counts.mean():.1f}")
        print(f"   Most active month: {monthly_counts.idxmax()} with {monthly_counts.max()} articles")
        
        # Day of week analysis
        self.df['day_of_week'] = self.df['date'].dt.day_name()
        dow_counts = self.df['day_of_week'].value_counts()
        print(f"\n📆 DAY OF WEEK ANALYSIS:")
        for day, count in dow_counts.items():
            print(f"   {day}: {count:,} articles ({count/len(self.df)*100:.1f}%)")
    
    def run_text_analysis(self):
        """Run comprehensive text analysis"""
        print("\n" + "="*60)
        print("🔤 TEXT ANALYSIS & TOPIC MODELING")
        print("="*60)
        
        # Add text features
        self.df = self.text_analyzer.analyze_headline_features(self.df)
        
        # Sentiment analysis
        print(f"\n😊 SENTIMENT ANALYSIS:")
        sentiment_cols = ['sentiment_compound', 'sentiment_positive', 'sentiment_negative', 'sentiment_neutral']
        for col in sentiment_cols:
            print(f"   {col}: {self.df[col].mean():.3f} (avg)")
        
        # Sentiment by company
        print(f"\n🏢 SENTIMENT BY COMPANY:")
        for company in TICKERS:
            company_data = self.df[self.df['stock'] == company]
            avg_sentiment = company_data['sentiment_compound'].mean()
            sentiment_label = "Positive" if avg_sentiment > 0.05 else "Negative" if avg_sentiment < -0.05 else "Neutral"
            print(f"   {company}: {avg_sentiment:.3f} ({sentiment_label})")
        
        # Topic analysis
        print(f"\n🏷️  TOPIC ANALYSIS:")
        print(f"   Avg topics per article: {self.df['topic_count'].mean():.1f}")
        
        # Keyword analysis by company
        self.text_analyzer.get_company_keyword_summary(self.df)
    
    def run_publisher_analysis(self):
        """Analyze publisher patterns"""
        if 'publisher' not in self.df.columns:
            return
            
        print("\n" + "="*60)
        print("🏢 PUBLISHER ANALYSIS")
        print("="*60)
        
        # Publisher domains (for email addresses)
        email_publishers = self.df[self.df['publisher'].str.contains('@', na=False)]
        if not email_publishers.empty:
            email_publishers['publisher_domain'] = email_publishers['publisher'].str.split('@').str[1]
            domain_counts = email_publishers['publisher_domain'].value_counts()
            
            print(f"\n📧 EMAIL PUBLISHER DOMAINS:")
            for domain, count in domain_counts.head(5).items():
                print(f"   {domain}: {count:,} articles")
        
        # Publisher specialization
        print(f"\n🎯 PUBLISHER SPECIALIZATION:")
        publisher_company_matrix = pd.crosstab(self.df['publisher'], self.df['stock'])
        top_publishers = self.df['publisher'].value_counts().head(3).index
        
        for publisher in top_publishers:
            publisher_data = self.df[self.df['publisher'] == publisher]
            top_company = publisher_data['stock'].value_counts().index[0]
            company_pct = (publisher_data['stock'] == top_company).mean() * 100
            print(f"   {publisher}: {publisher_data['stock'].nunique()} companies, "
                  f"specializes in {top_company} ({company_pct:.1f}%)")
    
    def generate_visualizations(self):
        """Generate EDA visualizations"""
        print("\n" + "="*60)
        print("📊 GENERATING VISUALIZATIONS")
        print("="*60)
        
        # Create visualization directory
        viz_dir = "output/eda_plots"
        os.makedirs(viz_dir, exist_ok=True)
        
        # 1. Articles by company
        plt.figure(figsize=(12, 6))
        company_counts = self.df['stock'].value_counts()
        plt.bar(company_counts.index, company_counts.values)
        plt.title('Number of Articles by Company')
        plt.xlabel('Company')
        plt.ylabel('Number of Articles')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{viz_dir}/articles_by_company.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Monthly article trends
        plt.figure(figsize=(14, 6))
        monthly_data = self.df.groupby(self.df['date'].dt.to_period('M')).size()
        monthly_data.index = monthly_data.index.astype(str)
        plt.plot(monthly_data.index, monthly_data.values, marker='o')
        plt.title('Monthly Article Frequency')
        plt.xlabel('Month')
        plt.ylabel('Number of Articles')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{viz_dir}/monthly_trends.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Sentiment distribution by company
        plt.figure(figsize=(12, 6))
        sentiment_by_company = self.df.groupby('stock')['sentiment_compound'].mean().sort_values()
        plt.bar(sentiment_by_company.index, sentiment_by_company.values)
        plt.title('Average Sentiment by Company')
        plt.xlabel('Company')
        plt.ylabel('Average Sentiment Score')
        plt.axhline(y=0, color='red', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(f'{viz_dir}/sentiment_by_company.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Visualizations saved to: {viz_dir}/")
    
    def run_complete_analysis(self):
        """Run complete EDA analysis"""
        if not self.load_and_validate():
            return
        
        print("🚀 STARTING COMPREHENSIVE EDA ANALYSIS")
        print(f"📊 Analyzing data for {len(TICKERS)} companies: {TICKERS}")
        
        # Run all analyses
        self.run_descriptive_analysis()
        self.run_time_series_analysis()
        self.run_text_analysis()
        self.run_publisher_analysis()
        self.generate_visualizations()
        
        print("\n" + "="*60)
        print("🎉 EDA ANALYSIS COMPLETE!")
        print("="*60)
        print(f"📈 Total articles analyzed: {len(self.df):,}")
        print(f"🏢 Companies covered: {self.df['stock'].nunique()}")
        print(f"📅 Analysis period: {self.df['date'].min().date()} to {self.df['date'].max().date()}")
        print(f"💡 Next: Check notebooks/ for detailed analysis")

def main():
    """Main function to run EDA analysis"""
    processor = EDAProcessor()
    processor.run_complete_analysis()

if __name__ == "__main__":
    main()