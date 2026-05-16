# config.py
# all the settings for the project live here so i'm not hardcoding stuff everywhere

DATA = {
    "universe": "SP500",
    "start_date": "2015-01-01",
    "end_date": "2024-12-31",
    "frequency": "daily",
    "data_dir": "data/raw",
    "cache_dir": "data/cache",
}

FACTORS = {
    "momentum_lookback": 252,     # 12 months of trading days
    "short_term_reversal": 21,    # skip last month in momentum calc
    "volatility_lookback": 63,    # 3 months for vol
    "value_lookback": 252,
    "quality_lookback": 252,
    "ic_window": 63,
    "zscore_clip": 3.0,           # clip outliers at +/- 3
}

PORTFOLIO = {
    "max_position_size": 0.05,    # no more than 5% in one stock
    "min_position_size": 0.001,
    "max_sector_weight": 0.25,
    "turnover_limit": 0.20,       # max 20% turnover each rebalance
    "rebalance_freq": "monthly",
    "target_vol": 0.10,           # 10% annualised vol target
    "leverage": 1.0,              # no leverage for now
    "transaction_cost_bps": 5,    # assuming 5bps round trip cost
}

# paper trading only - keys loaded from .env never hardcoded
ALPACA = {
    "api_key": "",
    "secret_key": "",
    "base_url": "https://paper-api.alpaca.markets",
}
