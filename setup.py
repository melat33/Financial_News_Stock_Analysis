from setuptools import setup, find_packages

setup(
    name="financial_news_stock_analysis",
    version="0.1.0",
    description="Financial News and Stock Analysis Dashboard",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "talib>=0.4.24",
        "jupyter>=1.0.0",
        "scipy>=1.7.0",
        "scikit-learn>=1.0.0",
    ],
    python_requires=">=3.8",
)