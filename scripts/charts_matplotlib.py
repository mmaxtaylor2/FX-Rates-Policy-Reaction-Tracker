"""
Charts (Matplotlib): FX & Rates Policy Reaction Tracker
Generates static visuals for multi-window event reactions.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_PATH = "data/event_reaction_output.csv"
SAVE_DIR = "charts"

def build_reaction_charts():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Run the pipeline first: python3 main.py")
    
    df = pd.read_csv(DATA_PATH)

    windows = ["Reaction_1D_%", "Reaction_3D_%", "Reaction_5D_%", "Reaction_10D_%"]

    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # Simple mean bar chart by window
    means = df[windows].mean()

    plt.figure(figsize=(8, 5))
    means.plot(kind="bar", title="Average FX & Rates Reaction by Window")
    plt.ylabel("Percent Change")
    plt.xlabel("Event Window")
    plt.tight_layout()
    plt.savefig(f"{SAVE_DIR}/reaction_window_averages.png")
    plt.close()

    # Bank-by-bank comparison
    banks = df["CentralBank"].unique()
    for bank in banks:
        sub = df[df["CentralBank"] == bank]

        if len(sub) == 0:
            continue

        means = sub[windows].mean()

        plt.figure(figsize=(8, 5))
        means.plot(kind="bar", title=f"{bank} - Average Reaction by Window")
        plt.ylabel("Percent Change")
        plt.xlabel("Event Window")
        plt.tight_layout()
        plt.savefig(f"{SAVE_DIR}/{bank}_reaction.png")
        plt.close()

    print("\nMatplotlib charts generated in /charts\n")

if __name__ == "__main__":
    build_reaction_charts()

