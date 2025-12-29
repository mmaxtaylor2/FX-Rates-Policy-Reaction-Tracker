"""
Yield Curve Reaction Engine (V2)
Measures policy reaction via:
- Short end (2Y proxy)
- Long end (10Y proxy)
- Curve slope change (2s10s) around policy events
"""

import pandas as pd
import yfinance as yf

# Proxy tickers:
# 2Y yield: ^IRX (not perfect but reliable proxy)
# 10Y yield: ^TNX
SHORT_TENOR = "^IRX"   # 3M / short-end proxy
LONG_TENOR  = "^TNX"   # 10Y Treasury

def build_yield_curve_reaction(events_df, days_back=180):
    # download yield history
    data = yf.download(
        [SHORT_TENOR, LONG_TENOR],
        period=f"{days_back}d",
        interval="1d",
        progress=False
    )["Close"].dropna()

    data.index = pd.to_datetime(data.index)

    # create slope measure
    data["Slope_2s10s"] = data[LONG_TENOR] - data[SHORT_TENOR]

    records = []
    for _, row in events_df.iterrows():
        date = pd.to_datetime(row["Date"])

        if date not in data.index:
            continue

        idx = data.index.get_loc(date)

        before = data.iloc[idx - 1] if idx-1 >= 0 else None
        after  = data.iloc[idx + 1] if idx+1 < len(data) else None

        if before is None or after is None:
            continue

        curve_move = after["Slope_2s10s"] - before["Slope_2s10s"]

        records.append({
            "Date": date.strftime("%Y-%m-%d"),
            "CentralBank": row["CentralBank"],
            "Decision": row["Decision"],
            "Short_End_Day0": before[SHORT_TENOR],
            "Long_End_Day0": before[LONG_TENOR],
            "Curve_Slope_Before": before["Slope_2s10s"],
            "Curve_Slope_After": after["Slope_2s10s"],
            "Slope_Change_bp": curve_move
        })

    return pd.DataFrame(records)

