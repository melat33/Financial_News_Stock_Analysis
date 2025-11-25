#!/usr/bin/env python3
"""
Task 2 - Price Data Download
Downloads stock price data for technical analysis
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.data_loader import DataLoader

def main():
    """Main function for Task 2"""
    print("🚀 TASK 2 - PRICE DATA DOWNLOAD")
    print("=" * 50)
    
    loader = DataLoader()
    
    # Download all price data
    price_data = loader.load_all_price_data()
    
    if not price_data.empty:
        print(f"\n✅ Task 2 completed!")
        print(f"📊 Downloaded data for {price_data['ticker'].nunique()} companies")
        print(f"📈 Total records: {len(price_data)}")
        print("Next: Run Task 3 analysis")
    else:
        print("❌ Task 2 failed - no price data downloaded")

if __name__ == "__main__":
    main()