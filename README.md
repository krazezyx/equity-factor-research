# Equity Factor Research
A systematic multi-factor equity research framework implementing cross-sectional signal construction, portfolio optimisation, and paper trading execution via the Alpaca Markets API.

## Overview
This repository implements a quantitative long-short equity strategy that exploits well-documented factor premia across the S&P 500 universe. The academic and practitioner literature consistently demonstrates that stocks exhibiting strong momentum, cheap valuations, high profitability, and low realised volatility earn excess returns that cannot be fully explained by market beta alone. This repo operationalises those signals into a production-grade research pipeline — from raw price and fundamental data through to backtested performance attribution and live paper trading execution.

## Research Hypothesis
The central hypothesis is that a composite factor score combining momentum, value, quality, and low-volatility signals — constructed on a cross-sectional, market-neutral basis and rebalanced monthly — generates statistically significant risk-adjusted returns (IR > 0.5) that persist out-of-sample across multiple market regimes, after accounting for realistic transaction costs and sector constraints. The thesis rests on the premise that these premia are behavioural and structural in origin, and therefore partially persistent, rather than artefacts of in-sample data mining.

## Methodology

### Factor Construction
- Momentum (12-1) — total return from month -12 to month -1, skipping the most recent month to avoid short-term reversal contamination.
- Value (Book-to-Price) — trailing book equity divided by market capitalisation, capturing mean-reversion in relative valuations.
- Quality (ROE + Gross Profitability) — return on equity and gross profit scaled by assets, following Novy-Marx (2013) and Fama-French (2015).
- Low-Volatility — realised annualised volatility computed over a 63-day trailing window, inverted so low-vol stocks score highest.

### Signal Aggregation
Each factor is cross-sectionally z-scored and winsorised at ±3 standard deviations to limit the influence of outliers. The four normalised scores are combined into an equal-weighted composite signal. Z-scoring is performed at each rebalance date within the current investment universe to ensure the signal is always market-relative and free of look-ahead bias.

### Portfolio Construction
The portfolio is constructed as a dollar-neutral long-short book using cvxpy as the optimisation backend. The objective maximises expected factor exposure (composite score) subject to a Ledoit-Wolf shrinkage covariance estimate for risk control, hard sector-neutrality constraints (max ±2% net sector exposure), a gross leverage cap of 1.0×, and individual position limits of ±5%. Rebalancing occurs monthly at the close.

### Risk Management
Portfolio volatility is targeted at 10% annualised via ex-ante scaling of position weights. Single-name position sizes are capped at 5% gross weight. One-way turnover is constrained to 20% per rebalance to limit market impact. Transaction costs are modelled at a flat 5 bps round-trip per name, applied directly in performance attribution rather than the optimisation objective to maintain convexity.

## Project Structure
equity-factor-research/
├── data/           # Data ingestion, cleaning, and local storage
├── factors/        # Factor signal construction and IC analysis
├── portfolio/      # Portfolio optimisation and position sizing
├── backtest/       # Backtesting engine and performance attribution
├── live/           # Alpaca Markets paper trading integration
├── research/       # Jupyter notebooks for exploratory analysis
├── tests/          # Unit tests
├── config.py       # Centralised settings for data, factors, portfolio, and API
├── .env.example    # Environment variable template (API credentials)
└── requirements.txt

## Stack
- Python 3.11
- pandas, numpy, scipy
- cvxpy (portfolio optimisation)
- scikit-learn (Ledoit-Wolf covariance shrinkage)
- statsmodels (factor regression, OLS attribution)
- yfinance (price and fundamental data)
- alphalens-reloaded (factor IC and tear sheets)
- pyfolio (portfolio performance attribution)
- Alpaca Markets API (paper trading execution)

## Results
Backtest results and factor IC analysis will be documented here as research progresses.

## Status
Active development — started May 2025.

## Disclaimer
This repository is a research project and is intended for educational and paper trading purposes only. Nothing in this codebase constitutes financial advice, an investment recommendation, or a solicitation to trade. All strategy testing is conducted on simulated paper trading accounts. Past performance of any modelled strategy does not guarantee future results.
