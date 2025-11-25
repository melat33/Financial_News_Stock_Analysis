# 🚀 QUICK CORRELATION NOTEBOOK
# =============================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("🚀 QUICK CORRELATION ANALYSIS")
print("=============================")

# Load the fixed merged data
merged = pd.read_csv('data/processed/merged_news_price.csv')
print(f"✅ Loaded {len(merged)} merged records")

# Quick correlation analysis
print("\n📊 CORRELATION RESULTS:")
correlations = []
for ticker in merged['ticker'].unique():
    data = merged[merged['ticker'] == ticker].dropna()
    if len(data) > 1:
        corr = data['sentiment'].corr(data['daily_return'])
        correlations.append({'ticker': ticker, 'correlation': corr, 'samples': len(data)})
        print(f"🏢 {ticker}: {corr:.3f} (n={len(data)})")

# Visualization
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
for t in merged['ticker'].unique():
    data = merged[merged['ticker'] == t].dropna()
    plt.scatter(data['sentiment'], data['daily_return'], alpha=0.7, label=t, s=50)
plt.xlabel('Sentiment')
plt.ylabel('Daily Returns')
plt.title('Sentiment vs Stock Returns')
plt.legend()

plt.subplot(1, 2, 2)
if correlations:
    corr_df = pd.DataFrame(correlations)
    plt.bar(corr_df['ticker'], corr_df['correlation'], color='lightblue')
    plt.xticks(rotation=45)
    plt.title('Correlation by Company')
    plt.ylabel('Correlation Coefficient')

plt.tight_layout()
plt.show()

print("\n🎉 NOTEBOOK READY FOR SUBMISSION!")