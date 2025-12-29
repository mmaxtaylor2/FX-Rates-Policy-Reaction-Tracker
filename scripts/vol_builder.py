import yfinance as yf
import pandas as pd
import os

# FX pairs to analyze
pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X"]

# Download 1 year of prices
raw = yf.download(pairs, period="1y", auto_adjust=True)

# Handle the MultiIndex structure correctly
if isinstance(raw.columns, pd.MultiIndex):
    prices = raw["Close"]
else:
    prices = raw

# 5-day rolling standard deviation as proxy IV
vol = prices.pct_change().rolling(5).std() * 100

# Prepare file format
vol = vol.reset_index()
vol.columns = ["Date"] + [c.replace("=X","_IV%") for c in vol.columns[1:]]

# Save
os.makedirs("data", exist_ok=True)
vol.to_csv("data/volatility_reaction.csv", index=False)

print("Volatility file generated:")
print(vol.head())

