# ---------------------------------------------------------------------------
# Data settings
# ---------------------------------------------------------------------------
DATA = {
    "universe": "SP500",          # equity universe to trade
    "start_date": "2015-01-01",   # backtest / research start date
    "end_date": "2024-12-31",     # backtest / research end date
    "frequency": "daily",         # bar frequency: daily | weekly | monthly
    "data_dir": "data/raw",       # path for raw data storage
    "cache_dir": "data/cache",    # path for processed / cached data
}

# ---------------------------------------------------------------------------
# Factor settings
# ---------------------------------------------------------------------------
FACTORS = {
    "momentum_lookback": 252,     # days for momentum signal (12-month)
    "short_term_reversal": 21,    # days for short-term reversal signal
    "volatility_lookback": 63,    # days for realised-volatility signal
    "value_lookback": 252,        # days for value / earnings-yield signal
    "quality_lookback": 252,      # days for quality / profitability signal
    "ic_window": 63,              # rolling IC calculation window (days)
    "zscore_clip": 3.0,           # winsorise factor z-scores at ±N
}

# ---------------------------------------------------------------------------
# Portfolio settings
# ---------------------------------------------------------------------------
PORTFOLIO = {
    "max_position_size": 0.05,    # max single-name weight (5%)
    "min_position_size": 0.001,   # min non-zero weight (0.1%)
    "max_sector_weight": 0.25,    # max weight in any one GICS sector
    "turnover_limit": 0.20,       # max one-way turnover per rebalance
    "rebalance_freq": "monthly",  # rebalance frequency: daily | weekly | monthly
    "target_vol": 0.10,           # annualised portfolio volatility target
    "leverage": 1.0,              # gross leverage cap
    "transaction_cost_bps": 5,    # assumed round-trip transaction cost (bps)
}

# ---------------------------------------------------------------------------
# API keys  (populate via environment variables — never commit real values)
# ---------------------------------------------------------------------------
ALPACA = {
    "api_key": "",                # set via env var ALPACA_API_KEY
    "secret_key": "",             # set via env var ALPACA_SECRET_KEY
    "base_url": "https://paper-api.alpaca.markets",  # paper trading endpoint
}
