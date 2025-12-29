"""
Plotly Interactive Charts for FX & Rates Policy Reaction Tracker
Creates interactive event study visuals for analysis & dashboard integration.
"""

import pandas as pd
import plotly.express as px
import os

DATA_PATH = "data/event_reaction_output.csv"
SAVE_DIR = "charts"

def build_interactive_charts():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Run main.py first to generate CSV data")

    df = pd.read_csv(DATA_PATH)
    windows = ["Reaction_1D_%", "Reaction_3D_%", "Reaction_5D_%", "Reaction_10D_%"]

    # Reaction by central bank
    fig1 = px.bar(
        df,
        x="CentralBank",
        y=windows,
        barmode="group",
        title="Policy Reaction by Central Bank (Interactive)",
    )
    fig1.write_html(f"{SAVE_DIR}/interactive_centralbank_reactions.html")

    # Reaction distribution
    fig2 = px.box(
        df,
        y=windows,
        title="Distribution of Event Reactions by Window",
    )
    fig2.write_html(f"{SAVE_DIR}/reaction_distribution.html")

    print("\nInteractive Plotly charts saved in /charts as HTML files.\n")

if __name__ == "__main__":
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    build_interactive_charts()

