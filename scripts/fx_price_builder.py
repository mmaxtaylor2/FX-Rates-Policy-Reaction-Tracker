import yfinance as yf
import pandas as pd
import os

pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X"]

# Download 1 year of price data (handles multi-index safely)
raw = yf.download(pairs, period="1y", auto_adjust=True)

# Case 1: MultiIndex DataFrame → Extract Close level
if isinstance(raw.columns, pd.MultiIndex):
    if ("Close" in raw.columns.levels[0]) or ("Close" in raw.columns):
        data = raw["Close"]
    else:
        # Fallback to use the last level if structure shifted
        data = raw.xs("Close", level=1, axis=1, drop_level=False)
else:
    # Case 2: Single index (rare)
    data = raw

data = data.reset_index()
data.columns = ["Date"] + list(data.columns[1:])  # Keep original pair names

os.makedirs("data", exist_ok=True)
data.to_csv("data/fx_prices.csv", index=False)

print("FX price data saved to: data/fx_prices.csv")
print(data.head())

