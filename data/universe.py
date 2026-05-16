import os 
import pandas as pd
import yfinance as yf


def get_sp500_tickers():
    # pulling the s&P 500 from wikipedia
    # first table on page is our full constituent list
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    try:
        tables = pd.read_html(url)
        df = tables[0]
    except Exception as e:
        raise RuntimeError (f"Unable to fetch S&P 500 tickers: {e}")
    tickers = df["Symbol"].tolist()

    # yfinance needs hyphens not dots 
    tickers = [t.replace(".","-") for t in tickers]

    return sorted(tickers)


def filter_universe(tickers, min_price = 5.0, min_volume = 500000):
    # downloading the last 30 days of financial data...
    print(f"downloading last {len(tickers)} tickers...")

    raw = yf.download(
        tickers,
        period = "30d",
        interval = "1d",
        auto_adjust = True,
        progress = False,
        threads = True
)

    close = raw["Close"]
    volume = raw["Volume"]

    passed = []
    removed = []

    for ticker in tickers:
        # will skip if yfinance returns empty
        if ticker not in close.columns:
            removed.append(ticker)
            continue

        avg_price = close[ticker].median()
        avg_vol = volume[ticker].median()

        # will remove cheap or low liquidity data
        if avg_price < min_price or avg_vol < min_volume:
            removed.append(ticker)
        else:
            passed.append(ticker)

    print(f"removed {len(removed)} tickers, {len(passed)} left")
    return sorted(passed)


def save_universe(tickers, filepath):
    # if folder does not exist -> I create
    os.makedirs(os.path.dirname(filepath), exist_ok = True)

    pd.DataFrame({"ticker": tickers}).to_csv(filepath, index = False)
    print(f"saved {len(tickers)} tickers to {filepath}")

if __name__ == "__main__":
    tickers = get_sp500_tickers()
    print(f"got {len(tickers)} tickers from Wikipedia")

    filtered = filter_universe(tickers)    
    save_universe(filtered, "data/raw/universe.csv")
