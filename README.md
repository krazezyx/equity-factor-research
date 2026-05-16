# Equity Factor Research

A multi-factor equity research project combining momentum, value, quality and low-volatility signals into a long-short strategy across the S&P 500.

## What this is

I built this to go beyond a simple backtest. Most student quant projects test one signal and call it done. This one constructs four separate alpha factors, combines them into a composite score, optimises a portfolio using proper risk controls, and runs it against live paper trading through the Alpaca API.

The full pipeline goes from raw price and fundamental data through to backtested performance attribution and live execution.

## Hypothesis

A composite factor score built from momentum, value, quality and low-volatility signals, rebalanced monthly on a market-neutral basis, generates risk-adjusted returns (IR > 0.5) that hold up out-of-sample across different market regimes once you account for transaction costs and sector constraints.

The bet is that these return premia are behavioural and structural in origin, not just data mining artifacts.

## Methodology

### Factor Construction
- Momentum (12-1) — return from month -12 to month -1, skipping the last month to avoid short-term reversal noise
- Value (Book-to-Price) — book equity divided by market cap, picks up mean reversion in valuations
- Quality (ROE + Gross Profitability) — based on Novy-Marx (2013) and Fama-French (2015)
- Low-Volatility — 63-day realised vol, inverted so lower vol scores higher

### Signal Aggregation
Each factor gets cross-sectionally z-scored and winsorised at 3 standard deviations to handle outliers. The four scores are combined equally. Z-scoring happens at each rebalance date so the signal is always relative to the current universe with no look-ahead bias.

### Portfolio Construction
Dollar-neutral long-short portfolio built with cvxpy. Maximises factor exposure subject to a Ledoit-Wolf covariance estimate, sector neutrality within 2%, gross leverage capped at 1x, and position limits of 5% per name.

### Risk Management
Volatility targeted at 10% annualised. Turnover capped at 20% per rebalance to control market impact. Transaction costs modelled at 5bps round-trip applied in performance attribution.

## Project Structure
```
equity-factor-research/
├── data/           # data ingestion, cleaning and storage
├── factors/        # factor signal construction and IC analysis
├── portfolio/      # optimisation and position sizing
├── backtest/       # backtesting engine and performance attribution
├── live/           # Alpaca paper trading integration
├── research/       # Jupyter notebooks
├── tests/          # unit tests
├── config.py       # settings for data, factors, portfolio and API
├── .env.example    # API credential template
└── requirements.txt
```

## Stack
Python 3.11, pandas, numpy, scipy, cvxpy, scikit-learn, statsmodels, yfinance, alphalens-reloaded, pyfolio, Alpaca Markets API

## Results
Backtest results and factor IC analysis will be added as the research develops.

## Status
Active development — started May 2025

## Disclaimer
Research project only. Not financial advice. All testing done on paper trading accounts.
