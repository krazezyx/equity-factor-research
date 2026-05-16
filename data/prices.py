import os
import pandas as pd
import yfinance as yf 


def download_prices(tickers, start, end):
  # downloading entire OHLCV history for each ticker (single batch)
  print(f"downloading price history for {len(tickers)} tickers...")

  raw = yf.download(
    tickers,
    start = start,
    end = end,
    interval = "1d",
    auto_adjust = True,
    progress = False,
    threads = True
  )

  # only need our closing price for calculating factor
  close = raw["Close"]

  return close


def clean_prices(close):
  # dropping tickers more than 20% of missing data
  threshold = 0.8
  close = close.dropna(axis = 1, thresh = int(len(close) * threshold))
  # forward fill gaps so our trading halts/missing days are handled
  close = close.ffill()

   # dropping our remaining NaNs at start
  close = close.dropna(how = "all")

  print(f"clean price matrix: {close.shape[0]} days x {close.shape[1]} tickers")

  return close


def save_prices(close, filepath):
  # create and save our folder as parquet for large matrices
  os.makedirs(os.path.dirname(filepath), exist_ok = True)
  close.to_parquet(filepath)
  print(f"saved price data to {filepath}")


if __name__ == "__main__":
  universe = pd.read_csv("data/raw/universe.csv")
  tickers = universe["ticker"].tolist()
  # bull market (2015-2019), crash (COVID 2020), recovery market (2020-2021), bear market(2022)...
  close = download_prices(tickers, start = "2015-01-01", end = "2024-12-31")
  close = clean_prices(close)
  save_prices(close, "data/raw/prices.parquet")
  
  
