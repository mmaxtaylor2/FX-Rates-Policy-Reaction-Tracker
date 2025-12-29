"""
Data Fetcher: Downloads FX and rates data for the Policy Reaction Tracker.
Uses Yahoo Finance daily close prices.
Updated for current yfinance behavior (no reliance on 'Adj Close').
"""

import yfinance as yf
import pandas as pd

def fetch_prices(tickers, days_back=180):
    """
    Downloads historical price data for the tickers provided.
    Default range: last 180 days, daily frequency.
    
    Parameters:
        tickers (list of str): Yahoo Finance tickers (e.g., ["EURUSD=X", "USDJPY=X"])
        days_back (int): Number of days of historical data to pull

    Returns:
        DataFrame with one column per ticker, indexed by date
    """

    # Request data
    data = yf.download(
        tickers,
        period=f"{days_back}d",
        interval="1d",
        progress=False
    )

    # Multi-ticker case: Yahoo returns a MultiIndex, so we extract Close prices
    if isinstance(data.columns, pd.MultiIndex):
        if "Close" in data.columns.levels[0]:
            close_prices = data["Close"].copy()
            close_prices.columns = [str(col) for col in close_prices.columns]
            close_prices.index = pd.to_datetime(close_prices.index, errors="coerce")
            return close_prices.dropna()

    # Single ticker case: "Close" will be a direct column
    if "Close" in data.columns:
        single = data["Close"].dropna()
        single.index = pd.to_datetime(single.index, errors="coerce")
        return single.to_frame()

    # If neither case applies, return a clear failure
    raise ValueError("Price data could not be fetched or formatted. Check tickers or internet connection.")

