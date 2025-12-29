import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ------------------------------------------------
# Page Setup
# ------------------------------------------------
st.set_page_config(page_title="FX & Rates Policy Reaction Dashboard", layout="wide")

# ------------------------------------------------
# Data Paths
# ------------------------------------------------
DATA_DIR = "data"
EVENT_FILE = os.path.join(DATA_DIR, "event_reaction_output.csv")
YIELD_FILE = os.path.join(DATA_DIR, "yield_curve_reaction.csv")
FX_FILE = os.path.join(DATA_DIR, "fx_prices.csv")
VOL_FILE = os.path.join(DATA_DIR, "volatility_reaction.csv")

# Load data
events = pd.read_csv(EVENT_FILE)
yc = pd.read_csv(YIELD_FILE)
fx = pd.read_csv(FX_FILE)
vol = pd.read_csv(VOL_FILE)

# ------------------------------------------------
# NAVIGATION (NO EMOJIS)
# ------------------------------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Overview", "FX Reactions", "Yield Curve", "Volatility", "Export PDF"]
)

# ------------------------------------------------
# Filters
# ------------------------------------------------
central_banks = sorted(events["CentralBank"].unique())
selected_bank = st.sidebar.selectbox("Central Bank", central_banks)

windows = [c for c in events.columns if "Reaction" in c]
selected_window = st.sidebar.selectbox("Event Window", windows)

# ------------------------------------------------
# PAGE: Overview
# ------------------------------------------------
if page == "Overview":
    st.title("FX & Rates Policy Reaction Dashboard")

    st.subheader(f"Policy Event Reactions: {selected_bank}")
    st.dataframe(
        events[events["CentralBank"] == selected_bank][["Date","Decision",selected_window]]
    )

    st.subheader("Yield Curve Transmission (2s10s Slope Change, bp)")
    st.dataframe(
        yc[yc["CentralBank"] == selected_bank][["Date","Decision","Slope_Change_bp"]]
    )

# ------------------------------------------------
# PAGE: FX Reactions
# ------------------------------------------------
elif page == "FX Reactions":
    st.title("FX Price Reactions")
    st.dataframe(events[events["CentralBank"] == selected_bank][["Date","Decision",selected_window]])

    st.subheader("FX Price Paths (Past Year)")
    plt.figure(figsize=(10,4))
    for col in fx.columns[1:]:
        plt.plot(fx["Date"], fx[col], label=col)
    plt.legend()
    st.pyplot(plt)

# ------------------------------------------------
# PAGE: Yield Curve (Comparison View)
# ------------------------------------------------
elif page == "Yield Curve":
    st.title("Yield Curve Impact Analysis")

    comparison = yc.pivot_table(
        index="Date",
        columns="CentralBank",
        values="Slope_Change_bp"
    )
    st.subheader("Cross-Central Bank Comparison: 2s10s Slope Change")
    st.dataframe(comparison)

    st.subheader(f"{selected_bank}: Detailed Curve Reactions")
    st.dataframe(yc[yc["CentralBank"] == selected_bank])

# ------------------------------------------------
# PAGE: Volatility Impact
# ------------------------------------------------
elif page == "Volatility":
    st.title("Volatility Shock vs Curve Transmission")

    merged = pd.merge(events, yc, on=["Date","CentralBank","Decision"])
    merged = pd.merge(merged, vol, on="Date")

    plt.figure(figsize=(6,4))
    plt.scatter(merged["EURUSD_IV%"], merged["Slope_Change_bp"])
    plt.xlabel("Volatility Change (%)")
    plt.ylabel("2s10s Slope Change (bp)")
    plt.title("Volatility Shock vs Yield Curve Reaction")
    st.pyplot(plt)

# ------------------------------------------------
# PAGE: PDF EXPORT (E)
# ------------------------------------------------
elif page == "Export PDF":
    st.title("Export Policy Reaction Note")

    st.write("Generate a formatted policy reaction summary as a PDF report:")

    if st.button("Generate PDF Report"):
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        file_path = "Policy_Reaction_Note.pdf"
        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "FX & Rates Policy Reaction Report")
        c.setFont("Helvetica", 12)
        c.drawString(50, 720, f"Central Bank: {selected_bank}")
        c.drawString(50, 700, f"Event Reaction Metric: {selected_window}")
        c.drawString(50, 680, "Generated from internal reaction dashboard data.")
        c.save()

        with open(file_path, "rb") as pdf:
            st.download_button("Download PDF Report", pdf, file_name=file_path)

    st.info("Click the button above to generate the report.")

