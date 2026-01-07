## FX & Rates Policy Reaction Tracker

A multi-asset dashboard for analyzing market reactions to central bank policy decisions.
Tracks FX spot moves, yield curve shifts, and volatility changes around policy events (Fed, ECB, BoE, BoC).

## Problem Context

Market reactions to central bank policy decisions are often discussed qualitatively, but comparing transmission across FX, rates, and volatility in a consistent, event-driven framework is nontrivial. This project was built to quantify how different central banks transmit policy signals across asset classes by standardizing event windows and measuring cross-asset responses around policy decisions.

## Live App
https://fx-rates-policy-reaction-tracker-ru45vwkrmjnwawnqdoqyct.streamlit.app

## Project Overview

This project simulates the workflow of a junior macro/FX research analyst:

Imports a calendar of central bank decisions
Builds event windows around each meeting (1D, 3D, 5D, 10D moves)
Measures FX spot reaction and front-end vs long-end rate shifts
Compares transmission across central banks
Generates a PDF policy reaction report

The output aims to replicate a simplified internal macro briefing tool.

## Key Features

Navigation dashboard by asset: Overview, FX, Yield Curve, Volatility, Export
Central bank comparison panel (cross-sectional slope reactions)
FX spot reaction measurements: EURUSD, GBPUSD, USDJPY
Yield curve impact using 2s10s slope (basis point change)
Volatility shock vs curve transmission scatter analysis
PDF export for use in reports, portfolios, and interview discussion

### Visualization Note

FX spot prices are displayed in absolute levels to preserve economic context (e.g., USDJPY vs EURUSD). Because FX pairs trade on different numerical scales, relative price movement comparisons may appear visually compressed for lower-level pairs. Event-window reaction metrics and tabular outputs should be used for cross-asset comparison.

## Architecture

FX-Rates-Policy-Reaction-Tracker/
│
├── main.py                         # Runs the pipeline and generates datasets
├── streamlit_app.py                # Front-end dashboard interface
│
├── data/                           # Generated outputs
│   ├── central_bank_events.csv
│   ├── event_reaction_output.csv
│   ├── yield_curve_reaction.csv
│   ├── fx_prices.csv
│   └── volatility_reaction.csv
│
├── scripts/                        # Processing modules
│   ├── pipeline.py
│   ├── data_fetcher.py
│   ├── event_engine.py
│   ├── yield_curve_engine.py
│   ├── vol_engine.py
│   └── fx_price_builder.py
│
└── requirements.txt                # Runtime dependencies

## How To Run

1. Create environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

2. Install dependencies
pip install -r requirements.txt

3. Generate data from the pipeline
python3 main.py

4. Launch dashboard
streamlit run streamlit_app.py

## Data Sources
FX spot prices: Yahoo Finance (EURUSD=X, GBPUSD=X, USDJPY=X)
Sovereign yields: Yahoo Finance government bond tickers
Volatility: ATM implied volatility proxies
Policy calendar: User-defined CSV (follows included schema)




