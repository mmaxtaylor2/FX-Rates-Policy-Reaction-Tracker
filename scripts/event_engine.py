"""
Event Engine: Multi-window event study generator.
Stores scalar values to allow charting and statistical analysis.
"""

import pandas as pd

WINDOWS = [1, 3, 5, 10]

def generate_event_windows(events_df, price_df):
    price_df.index = pd.to_datetime(price_df.index, errors="coerce")
    events_df["Date"] = pd.to_datetime(events_df["Date"], errors="coerce")

    records = []

    for _, row in events_df.iterrows():
        event_date = row["Date"]
        bank = row["CentralBank"]
        decision = row["Decision"]

        if event_date not in price_df.index:
            continue

        idx = price_df.index.get_loc(event_date)

        row_data = {
            "Date": event_date.strftime("%Y-%m-%d"),
            "CentralBank": bank,
            "Decision": decision
        }

        for w in WINDOWS:
            before_idx = idx - w
            after_idx  = idx + w

            if before_idx < 0 or after_idx >= len(price_df):
                break

            px_before = price_df.iloc[before_idx]
            px_after  = price_df.iloc[after_idx]

            # Compute mean % reaction across assets
            reaction = ((px_after - px_before) / px_before) * 100
            reaction_mean = reaction.mean()  # <-- scalar number

            row_data[f"Reaction_{w}D_%"] = reaction_mean

        if len(row_data) > 3:  # ensure data was added
            records.append(row_data)

    return pd.DataFrame(records)

