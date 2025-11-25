# scripts/quick_check.py
from pathlib import Path

def quick_check():
    base = Path(__file__).parent.parent
    print("🔍 Quick file check:")
    
    # Check news files
    news_files = list((base / "data" / "raw").glob("*news*.csv"))
    print(f"\n📰 News files in data/raw/:")
    for f in news_files:
        print(f"   - {f.name}")
    
    # Check stock files
    stock_dirs = ["raw", "price"]
    for dir_name in stock_dirs:
        stock_dir = base / "data" / dir_name
        if stock_dir.exists():
            stock_files = list(stock_dir.glob("*.csv"))
            print(f"\n📈 Stock files in data/{dir_name}/:")
            for f in stock_files:
                if "news" not in f.name.lower():
                    print(f"   - {f.name}")

if __name__ == "__main__":
    quick_check()