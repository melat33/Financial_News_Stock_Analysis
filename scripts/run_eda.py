#!/usr/bin/env python3
"""
Enhanced EDA Runner Script with Better Error Handling
Task 1: Comprehensive EDA for Financial News Analysis
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

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import load_news_data, validate_news_data
from src.text_analyzer import TextAnalyzer
from src.config import TICKERS

class EDAProcessor:
    def __init__(self):
        self.df = None
        self.text_analyzer = TextAnalyzer()
        
        # Company colors for consistent visualizations
        self.company_colors = {
            'AAPL': '#A2AAAD', 'AMZN': '#FF9900', 'GOOG': '#4285F4', 
            'META': '#1877F2', 'MSFT': '#737373', 'NVDA': '#76B900'
        }
        
        # Visualization settings
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Create output directories
        self.setup_directories()
    
    def setup_directories(self):
        """Create necessary output directories"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.viz_dir = os.path.join(base_dir, "output", "eda_plots")
        self.data_dir = os.path.join(base_dir, "data", "processed")
        
        os.makedirs(self.viz_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        print(f"📁 Output directories created:")
        print(f"   • Visualizations: {self.viz_dir}")
        print(f"   • Processed data: {self.data_dir}")
    
    def load_and_validate(self):
        """Load and validate news data with enhanced error handling"""
        print("📥 LOADING NEWS DATA...")
        print("=" * 60)
        
        try:
            self.df = load_news_data()
            if self.df is not None:
                self.df = validate_news_data(self.df)
                print("✅ Data loaded and validated successfully")
                return True
            else:
                print("❌ Failed to load data")
                return False
                
        except Exception as e:
            print(f"❌ Error in data loading: {e}")
            return False
    
    def run_descriptive_analysis(self):
        """Run comprehensive descriptive analysis"""
        print("\n" + "="*60)
        print("📊 DESCRIPTIVE STATISTICS ANALYSIS")
        print("="*60)
        
        try:
            # Basic statistics
            print(f"\n📈 BASIC STATISTICS:")
            print(f"   Total articles: {len(self.df):,}")
            print(f"   Date range: {self.df['date'].min()} to {self.df['date'].max()}")
            print(f"   Days covered: {(self.df['date'].max() - self.df['date'].min()).days} days")
            print(f"   Companies analyzed: {self.df['stock'].nunique()}")
            
            # Articles by company
            print(f"\n🏢 ARTICLES BY COMPANY:")
            company_counts = self.df['stock'].value_counts()
            for company, count in company_counts.items():
                percentage = (count / len(self.df)) * 100
                print(f"   {company}: {count:,} articles ({percentage:.1f}%)")
            
            # Text statistics
            print(f"\n🔤 TEXT STATISTICS:")
            print(f"   Avg headline length: {self.df['headline_length'].mean():.1f} chars")
            print(f"   Avg word count: {self.df['word_count'].mean():.1f} words")
            print(f"   Max headline length: {self.df['headline_length'].max()} chars")
            print(f"   Min headline length: {self.df['headline_length'].min()} chars")
            
            # Publisher analysis
            if 'publisher' in self.df.columns:
                print(f"\n📰 PUBLISHER ANALYSIS:")
                publisher_counts = self.df['publisher'].value_counts()
                print(f"   Total publishers: {len(publisher_counts)}")
                print(f"   Top 5 publishers:")
                for i, (pub, count) in enumerate(publisher_counts.head(5).items(), 1):
                    percentage = (count / len(self.df)) * 100
                    print(f"     {i}. {pub}: {count:,} articles ({percentage:.1f}%)")
                    
            return True
            
        except Exception as e:
            print(f"❌ Error in descriptive analysis: {e}")
            return False
    
    def run_time_series_analysis(self):
        """Analyze news frequency over time"""
        print("\n" + "="*60)
        print("⏰ TIME SERIES ANALYSIS")
        print("="*60)
        
        try:
            # Daily article count
            daily_counts = self.df.groupby(self.df['date'].dt.date).size()
            
            print(f"\n📅 DAILY FREQUENCY:")
            print(f"   Avg articles per day: {daily_counts.mean():.1f}")
            print(f"   Max articles in one day: {daily_counts.max()}")
            print(f"   Min articles in one day: {daily_counts.min()}")
            print(f"   Busiest day: {daily_counts.idxmax()} with {daily_counts.max()} articles")
            print(f"   Days with news: {len(daily_counts)}")
            print(f"   Days without news: {(self.df['date'].max() - self.df['date'].min()).days - len(daily_counts) + 1}")
            
            # Monthly trends
            monthly_counts = self.df.groupby(self.df['date'].dt.to_period('M')).size()
            print(f"\n📈 MONTHLY TRENDS:")
            print(f"   Avg articles per month: {monthly_counts.mean():.1f}")
            print(f"   Most active month: {monthly_counts.idxmax()} with {monthly_counts.max()} articles")
            print(f"   Least active month: {monthly_counts.idxmin()} with {monthly_counts.min()} articles")
            
            # Day of week analysis
            self.df['day_of_week'] = self.df['date'].dt.day_name()
            dow_counts = self.df['day_of_week'].value_counts()
            print(f"\n📆 DAY OF WEEK ANALYSIS:")
            for day, count in dow_counts.items():
                percentage = (count / len(self.df)) * 100
                print(f"   {day}: {count:,} articles ({percentage:.1f}%)")
                
            return True
            
        except Exception as e:
            print(f"❌ Error in time series analysis: {e}")
            return False
    
    def run_text_analysis(self):
        """Run comprehensive text analysis with error handling"""
        print("\n" + "="*60)
        print("🔤 TEXT ANALYSIS & TOPIC MODELING")
        print("="*60)
        
        try:
            # Add text features
            print("   📝 Processing text features...")
            self.df = self.text_analyzer.analyze_headline_features(self.df)
            
            # Sentiment analysis
            print(f"\n😊 SENTIMENT ANALYSIS:")
            sentiment_cols = ['sentiment_compound', 'sentiment_positive', 'sentiment_negative', 'sentiment_neutral']
            
            for col in sentiment_cols:
                if col in self.df.columns:
                    mean_val = self.df[col].mean()
                    std_val = self.df[col].std()
                    print(f"   {col}: {mean_val:.3f} ± {std_val:.3f} (mean ± std)")
            
            # Sentiment by company
            print(f"\n🏢 SENTIMENT BY COMPANY:")
            for company in TICKERS:
                company_data = self.df[self.df['stock'] == company]
                if len(company_data) > 0 and 'sentiment_compound' in company_data.columns:
                    avg_sentiment = company_data['sentiment_compound'].mean()
                    if avg_sentiment > 0.05:
                        sentiment_label = "Positive"
                    elif avg_sentiment < -0.05:
                        sentiment_label = "Negative"
                    else:
                        sentiment_label = "Neutral"
                    print(f"   {company}: {avg_sentiment:.3f} ({sentiment_label})")
            
            # Topic analysis
            if 'topic_count' in self.df.columns:
                print(f"\n🏷️  TOPIC ANALYSIS:")
                print(f"   Avg topics per article: {self.df['topic_count'].mean():.1f}")
                print(f"   Max topics in article: {self.df['topic_count'].max()}")
                print(f"   Articles with 0 topics: {(self.df['topic_count'] == 0).sum()} ({(self.df['topic_count'] == 0).mean()*100:.1f}%)")
            
            # Keyword analysis by company
            print(f"\n🔍 KEYWORD ANALYSIS BY COMPANY:")
            self.text_analyzer.get_company_keyword_summary(self.df)
            
            return True
            
        except Exception as e:
            print(f"❌ Error in text analysis: {e}")
            print("💡 Continuing with basic analysis...")
            return False
    
    def run_publisher_analysis(self):
        """Analyze publisher patterns"""
        if 'publisher' not in self.df.columns:
            print("ℹ️  No publisher data available for analysis")
            return True
            
        print("\n" + "="*60)
        print("🏢 PUBLISHER ANALYSIS")
        print("="*60)
        
        try:
            # Publisher domains (for email addresses)
            email_publishers = self.df[self.df['publisher'].str.contains('@', na=False)]
            if not email_publishers.empty:
                email_publishers = email_publishers.copy()
                email_publishers['publisher_domain'] = email_publishers['publisher'].str.split('@').str[1]
                domain_counts = email_publishers['publisher_domain'].value_counts()
                
                print(f"\n📧 EMAIL PUBLISHER DOMAINS:")
                for domain, count in domain_counts.head(5).items():
                    percentage = (count / len(email_publishers)) * 100
                    print(f"   {domain}: {count:,} articles ({percentage:.1f}% of email articles)")
            
            # Publisher specialization
            print(f"\n🎯 PUBLISHER SPECIALIZATION:")
            publisher_company_matrix = pd.crosstab(self.df['publisher'], self.df['stock'])
            top_publishers = self.df['publisher'].value_counts().head(5).index
            
            for publisher in top_publishers:
                publisher_data = self.df[self.df['publisher'] == publisher]
                if len(publisher_data) > 0:
                    top_company = publisher_data['stock'].value_counts().index[0]
                    company_pct = (publisher_data['stock'] == top_company).mean() * 100
                    print(f"   {publisher}: {publisher_data['stock'].nunique()} companies, "
                          f"specializes in {top_company} ({company_pct:.1f}%)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error in publisher analysis: {e}")
            return False
    
    def generate_visualizations(self):
        """Generate EDA visualizations with proper path handling"""
        print("\n" + "="*60)
        print("📊 GENERATING VISUALIZATIONS")
        print("="*60)
        
        print(f"📁 Saving visualizations to: {self.viz_dir}")
        
        try:
            # 1. Articles by company
            plt.figure(figsize=(12, 6))
            company_counts = self.df['stock'].value_counts()
            colors = [self.company_colors.get(company, 'gray') for company in company_counts.index]
            bars = plt.bar(company_counts.index, company_counts.values, color=colors, alpha=0.8)
            
            plt.title('Number of Articles by Company', fontsize=14, fontweight='bold')
            plt.xlabel('Company', fontweight='bold')
            plt.ylabel('Number of Articles', fontweight='bold')
            plt.xticks(rotation=45)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                        f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(os.path.join(self.viz_dir, 'articles_by_company.png'), dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✅ Created: articles_by_company.png")
            
            # 2. Monthly article trends
            plt.figure(figsize=(14, 6))
            monthly_data = self.df.groupby(self.df['date'].dt.to_period('M')).size()
            monthly_data.index = monthly_data.index.astype(str)
            plt.plot(monthly_data.index, monthly_data.values, marker='o', linewidth=2, color='steelblue')
            plt.title('Monthly Article Frequency', fontsize=14, fontweight='bold')
            plt.xlabel('Month', fontweight='bold')
            plt.ylabel('Number of Articles', fontweight='bold')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(os.path.join(self.viz_dir, 'monthly_trends.png'), dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✅ Created: monthly_trends.png")
            
            # 3. Headline length distribution
            plt.figure(figsize=(10, 6))
            plt.hist(self.df['headline_length'], bins=50, color='lightcoral', alpha=0.7, edgecolor='black')
            plt.axvline(self.df['headline_length'].mean(), color='red', linestyle='--', linewidth=2, 
                       label=f'Mean: {self.df["headline_length"].mean():.1f}')
            plt.title('Distribution of Headline Lengths', fontsize=14, fontweight='bold')
            plt.xlabel('Headline Length (characters)', fontweight='bold')
            plt.ylabel('Frequency', fontweight='bold')
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(self.viz_dir, 'headline_length_distribution.png'), dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✅ Created: headline_length_distribution.png")
            
            # 4. Word count distribution
            plt.figure(figsize=(10, 6))
            plt.hist(self.df['word_count'], bins=30, color='lightgreen', alpha=0.7, edgecolor='black')
            plt.axvline(self.df['word_count'].mean(), color='green', linestyle='--', linewidth=2, 
                       label=f'Mean: {self.df["word_count"].mean():.1f}')
            plt.title('Distribution of Word Counts', fontsize=14, fontweight='bold')
            plt.xlabel('Word Count', fontweight='bold')
            plt.ylabel('Frequency', fontweight='bold')
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(self.viz_dir, 'word_count_distribution.png'), dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✅ Created: word_count_distribution.png")
            
            # 5. Sentiment distribution by company (if sentiment data exists)
            if 'sentiment_compound' in self.df.columns:
                plt.figure(figsize=(12, 6))
                sentiment_by_company = self.df.groupby('stock')['sentiment_compound'].mean().sort_values()
                colors = [self.company_colors.get(company, 'gray') for company in sentiment_by_company.index]
                bars = plt.bar(sentiment_by_company.index, sentiment_by_company.values, color=colors, alpha=0.8)
                
                plt.title('Average Sentiment by Company', fontsize=14, fontweight='bold')
                plt.xlabel('Company', fontweight='bold')
                plt.ylabel('Average Sentiment Score', fontweight='bold')
                plt.axhline(y=0, color='red', linestyle='--', alpha=0.7)
                plt.xticks(rotation=45)
                
                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2., height + (0.01 if height >= 0 else -0.01),
                            f'{height:.3f}', ha='center', va='bottom' if height >= 0 else 'top', fontweight='bold')
                
                plt.tight_layout()
                plt.savefig(os.path.join(self.viz_dir, 'sentiment_by_company.png'), dpi=300, bbox_inches='tight')
                plt.close()
                print("   ✅ Created: sentiment_by_company.png")
            
            # 6. Day of week pattern
            plt.figure(figsize=(10, 6))
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_counts = self.df['day_of_week'].value_counts().reindex(day_order)
            bars = plt.bar(day_counts.index, day_counts.values, color='lightblue', alpha=0.7)
            
            plt.title('Articles by Day of Week', fontsize=14, fontweight='bold')
            plt.xlabel('Day of Week', fontweight='bold')
            plt.ylabel('Number of Articles', fontweight='bold')
            plt.xticks(rotation=45)
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                        f'{int(height):,}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(os.path.join(self.viz_dir, 'articles_by_day_of_week.png'), dpi=300, bbox_inches='tight')
            plt.close()
            print("   ✅ Created: articles_by_day_of_week.png")
            
            print(f"\n✅ All visualizations saved to: {self.viz_dir}")
            print(f"   📊 Generated {len([f for f in os.listdir(self.viz_dir) if f.endswith('.png')])} visualization files")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating visualizations: {e}")
            return False
    
    def save_processed_data(self):
        """Save processed data for future analysis"""
        print("\n💾 SAVING PROCESSED DATA...")
        
        try:
            output_file = os.path.join(self.data_dir, "eda_processed_data.csv")
            self.df.to_csv(output_file, index=False)
            print(f"✅ Processed data saved to: {output_file}")
            print(f"   📁 File size: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")
            print(f"   📊 Records: {len(self.df):,} articles")
            return True
            
        except Exception as e:
            print(f"❌ Error saving processed data: {e}")
            return False
    
    def generate_summary_report(self):
        """Generate final summary report"""
        print("\n" + "="*60)
        print("📋 EDA SUMMARY REPORT")
        print("="*60)
        
        try:
            # Key metrics
            total_articles = len(self.df)
            date_range = f"{self.df['date'].min().strftime('%Y-%m-%d')} to {self.df['date'].max().strftime('%Y-%m-%d')}"
            companies_covered = self.df['stock'].nunique()
            avg_daily_articles = total_articles / (self.df['date'].max() - self.df['date'].min()).days
            
            print(f"🎯 KEY METRICS:")
            print(f"   • Total Articles Analyzed: {total_articles:,}")
            print(f"   • Analysis Period: {date_range}")
            print(f"   • Companies Covered: {companies_covered}")
            print(f"   • Average Daily Articles: {avg_daily_articles:.1f}")
            print(f"   • Data Quality: {'GOOD' if not self.df.isnull().any().any() else 'REVIEW REQUIRED'}")
            
            # Most covered company
            most_covered = self.df['stock'].value_counts().index[0]
            least_covered = self.df['stock'].value_counts().index[-1]
            
            print(f"\n🏢 COVERAGE INSIGHTS:")
            print(f"   • Most Covered: {most_covered}")
            print(f"   • Least Covered: {least_covered}")
            
            # Text insights
            if 'sentiment_compound' in self.df.columns:
                avg_sentiment = self.df['sentiment_compound'].mean()
                sentiment_trend = "Positive" if avg_sentiment > 0.05 else "Negative" if avg_sentiment < -0.05 else "Neutral"
                print(f"\n😊 SENTIMENT OVERVIEW:")
                print(f"   • Overall Sentiment: {sentiment_trend} ({avg_sentiment:.3f})")
                print(f"   • Headline Diversity: {self.df['headline_length'].std():.1f} chars std dev")
            
            print(f"\n📈 NEXT STEPS:")
            print(f"   1. Review visualizations in: {self.viz_dir}")
            print(f"   2. Check processed data in: {self.data_dir}")
            print(f"   3. Proceed to Task 2: Quantitative Analysis")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating summary: {e}")
            return False
    
    def run_complete_analysis(self):
        """Run complete EDA analysis"""
        print("🚀 STARTING COMPREHENSIVE EDA ANALYSIS")
        print("=" * 60)
        print(f"📊 Analyzing data for {len(TICKERS)} companies: {TICKERS}")
        print("=" * 60)
        
        # Track success of each step
        steps_completed = 0
        total_steps = 7
        
        # Step 1: Load and validate data
        if self.load_and_validate():
            steps_completed += 1
            
            # Step 2: Descriptive analysis
            if self.run_descriptive_analysis():
                steps_completed += 1
            
            # Step 3: Time series analysis
            if self.run_time_series_analysis():
                steps_completed += 1
            
            # Step 4: Text analysis
            if self.run_text_analysis():
                steps_completed += 1
            
            # Step 5: Publisher analysis
            if self.run_publisher_analysis():
                steps_completed += 1
            
            # Step 6: Generate visualizations
            if self.generate_visualizations():
                steps_completed += 1
            
            # Step 7: Save data and generate report
            if self.save_processed_data() and self.generate_summary_report():
                steps_completed += 1
        
        # Final summary
        print("\n" + "="*60)
        print("🎉 EDA ANALYSIS COMPLETED!")
        print("="*60)
        print(f"📈 Progress: {steps_completed}/{total_steps} steps completed")
        
        if steps_completed >= 5:
            print("✅ SUCCESS: Comprehensive EDA analysis finished")
            print("💡 Next: Explore detailed analysis in notebooks/ folder")
        else:
            print("⚠️  PARTIAL: Some analysis steps encountered issues")
            print("🔧 Check error messages above and review data quality")
        
        print(f"\n📁 Output Locations:")
        print(f"   • Visualizations: {self.viz_dir}")
        print(f"   • Processed Data: {self.data_dir}")
        print("="*60)

def main():
    """Main function to run EDA analysis"""
    try:
        processor = EDAProcessor()
        processor.run_complete_analysis()
    except KeyboardInterrupt:
        print("\n❌ Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Check your data and configuration files")

if __name__ == "__main__":
    main()