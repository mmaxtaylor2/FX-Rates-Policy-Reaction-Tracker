"""
Pipeline: FX & Rates Policy Reaction Tracker
Coordinates full workflow:
1. Load event calendar
2. Download FX & rates close prices
3. Build multi-window FX & rate reactions (1D, 3D, 5D, 10D)
4. Measure yield curve slope reaction (short vs long end)
5. Save output files to /data
"""

import os
import pandas as pd

from scripts.data_fetcher import fetch_prices
from scripts.event_engine import generate_event_windows
from scripts.yield_curve_engine import build_yield_curve_reaction


def run_event_reaction_pipeline():
    # ------------------------------------------------
    # 1. Load event calendar
    # ------------------------------------------------
    print("\n[1] Loading event calendar...")
    events_path = "data/central_bank_events.csv"

    if not os.path.exists(events_path):
        raise FileNotFoundError("Missing file: data/central_bank_events.csv")

    events = pd.read_csv(events_path)
    print(f"Loaded {len(events)} policy events")

    # ------------------------------------------------
    # 2. Fetch FX + rates market data
    # ------------------------------------------------
    print("\n[2] Fetching FX and rates data...")
    tickers = ["EURUSD=X", "USDJPY=X", "GBPUSD=X", "^TNX"]  # FX + 10Y treasury proxy
    prices = fetch_prices(tickers)
    print("Market data downloaded")

    # ------------------------------------------------
    # 3. Multi-window FX & rates reaction (1D, 3D, 5D, 10D)
    # ------------------------------------------------
    print("\n[3] Building event windows (1D, 3D, 5D, 10D)...")
    event_output = generate_event_windows(events, prices)
    event_output_path = "data/event_reaction_output.csv"
    event_output.to_csv(event_output_path, index=False)
    print(f"Event window results saved to {event_output_path}")

    # ------------------------------------------------
    # 4. Yield curve slope reaction (short-end vs long-end)
    # ------------------------------------------------
    print("\n[4] Measuring yield curve reaction...")
    yield_df = build_yield_curve_reaction(events)
    yield_output_path = "data/yield_curve_reaction.csv"
    yield_df.to_csv(yield_output_path, index=False)
    print(f"Yield curve reactions saved to {yield_output_path}")

    # ------------------------------------------------
    # 5. Completion notice
    # ------------------------------------------------
    print("\n--- Pipeline completed successfully. ---\n")

