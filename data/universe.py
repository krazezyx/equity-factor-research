"""
data/universe.py
----------------
S&P 500 universe construction: fetch constituents, apply liquidity filters,
and persist the investable universe to disk.
"""

import os
import pandas as pd
import yfinance as yf


def get_sp500_tickers() -> list[str]:
    """Scrape the current S&P 500 constituent list from Wikipedia.

    Parses the first table on the S&P 500 Wikipedia page, which is
    maintained by the Wikimedia community and updated when index
    changes are announced.

    Returns
    -------
    list[str]
        Sorted list of ticker symbols formatted for yfinance
        (dots replaced with hyphens, e.g. BRK.B -> BRK-B).

    Raises
    ------
    RuntimeError
        If the Wikipedia page cannot be fetched or parsed.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    try:
        # read_html returns a list of all tables on the page;
        # the first table is always the constituent list
        tables = pd.read_html(url, header=0)
        df = tables[0]
    except Exception as exc:
        raise RuntimeError(
            f"Failed to fetch S&P 500 constituents from Wikipedia: {exc}"
        ) from exc

    # Column is labelled "Symbol" on the Wikipedia table
    tickers = df["Symbol"].tolist()

    # yfinance uses hyphens where exchanges use dots (e.g. BRK.B -> BRK-B)
    tickers = [t.replace(".", "-") for t in tickers]

    return sorted(tickers)


def filter_universe(
    tickers: list[str],
    min_price: float = 5.0,
    min_volume: int = 500_000,
) -> list[str]:
    """Remove illiquid and low-priced names from the ticker list.

    Downloads 30 calendar days of daily OHLCV data for all tickers in
    a single batched yfinance call, then applies two independent filters:

    1. **Price filter** — drops tickers whose median closing price over
       the window is below ``min_price``. Eliminates de-facto penny
       stocks that may still technically be in the index.

    2. **Volume filter** — drops tickers whose median daily dollar-volume
       is below ``min_volume``. Eliminates names with insufficient
       liquidity to trade at reasonable market impact.

    Parameters
    ----------
    tickers : list[str]
        Raw ticker list, typically the output of ``get_sp500_tickers()``.
    min_price : float, optional
        Minimum acceptable median closing price in USD. Default 5.0.
    min_volume : int, optional
        Minimum acceptable median daily share volume. Default 500,000.

    Returns
    -------
    list[str]
        Filtered and sorted list of tickers that pass both screens.
    """
    print(f"Downloading 30-day price/volume data for {len(tickers)} tickers...")

    # Batch download is far faster than looping; auto_adjust=True returns
    # split- and dividend-adjusted closes so the price screen is meaningful
    raw = yf.download(
        tickers,
        period="30d",
        interval="1d",
        auto_adjust=True,
        progress=False,
        threads=True,
    )

    close = raw["Close"]
    volume = raw["Volume"]

    removed_price: list[str] = []
    removed_volume: list[str] = []
    passed: list[str] = []

    for ticker in tickers:
        # A ticker may be missing entirely if yfinance couldn't fetch it
        if ticker not in close.columns:
            removed_price.append(ticker)
            continue

        median_close = close[ticker].median()
        median_vol = volume[ticker].median()

        if median_close < min_price:
            removed_price.append(ticker)
        elif median_vol < min_volume:
            removed_volume.append(ticker)
        else:
            passed.append(ticker)

    # Report what was cut and why
    if removed_price:
        print(
            f"  Removed {len(removed_price)} ticker(s) — price below "
            f"${min_price:.2f} or data unavailable: {removed_price}"
        )
    if removed_volume:
        print(
            f"  Removed {len(removed_volume)} ticker(s) — median daily volume "
            f"below {min_volume:,}: {removed_volume}"
        )

    print(f"  Universe after filtering: {len(passed)} tickers (started with {len(tickers)})")

    return sorted(passed)


def save_universe(tickers: list[str], filepath: str) -> None:
    """Persist the filtered ticker list to a single-column CSV file.

    Creates any intermediate directories in ``filepath`` if they do not
    already exist, so callers do not need to pre-create the output path.

    Parameters
    ----------
    tickers : list[str]
        Filtered universe to save.
    filepath : str
        Destination path including filename, e.g. ``"data/raw/universe.csv"``.
    """
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    pd.DataFrame({"ticker": tickers}).to_csv(filepath, index=False)

    print(f"Saved {len(tickers)} tickers to {filepath}")


if __name__ == "__main__":
    OUTPUT_PATH = "data/raw/universe.csv"

    tickers = get_sp500_tickers()
    print(f"Fetched {len(tickers)} S&P 500 constituents from Wikipedia.")

    filtered = filter_universe(tickers)

    save_universe(filtered, OUTPUT_PATH)
