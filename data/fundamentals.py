import os
import pandas as pd
import yfinance as yf


def get_fundamentals(tickers):
  # we are looping through each ticker and pulling key balance sheets/income data
  records = []

  for i, ticker in enumerate(tickers):
    try:
      stock = yf.Ticker(ticker)
      info = stock.info

      records.append({
        "ticker": ticker,
        "book_value": info.get("bookValue", None),
        "market_cap": info.get("marketCap", None),
        "roe": info.get("returnOnEquity", None),
        "gross_profit": info.get("grossProfits", None),
        "total_assets": info.get("totalAssets", None)
      })

      # printing progress for every 50 tickers to know its working
      if (i+1) % 50 == 0:
        print(f"fetched {i + 1} / {len(tickers)}")

    except Exception as e:
      print(f"failed on {ticker}: {e}")
      continue

  df = pd.DataFrame(records)
  return df


def clean_fundamentals(df):
  # dropping rows that contain NULL book value/market cap
  # cant calculate value factor without these two
  df = df.dropna(subset =["book_value", "market_cap"])

  df["book_to_price"] = df["book_value"] / (df["market_cap"] / 1e9)
  df["gross_profitability"] = df["gross_profit"] / df["total_assets"]

  df = df[df["book_to_price"] > 0]

  print(f"got clean fundamentals for {len(df)} tickers")
  return df


def save_fundamentals(df, filepath):
  os.makedirs(os.path.dirname(filepath), exist_ok = True)
  df.to_csv(filepath, index = False)
  print(f"saved fundamentals to {filepath}")


if __name__ == "__main__":
  universe = pd.read_csv("data/raw/universe.csv")
  tickers = universe["ticker"].tolist()

  df = get_fundamentals(tickers)
  df = clean_fundamentals(df)
  save_fundamentals(df, "data/raw/fundamentals.csv")
  

  
