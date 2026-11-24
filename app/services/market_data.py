"""
Market data service for fetching historical data.
"""
import pandas as pd
import yfinance as yf
from datetime import datetime


class MarketDataService:
    """
    Service for fetching market data from various sources.
    """

    def __init__(self, provider: str = "yahoo"):
        """
        Initialize market data service.

        Args:
            provider: Data provider (currently only 'yahoo' supported)
        """
        self.provider = provider

    def get_historical_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        Fetch historical market data.

        Args:
            symbol: Trading symbol
            start_date: Start date
            end_date: End date
            interval: Data interval (1d, 1h, etc.)

        Returns:
            DataFrame with OHLCV data
        """
        if self.provider == "yahoo":
            return self._fetch_yahoo_data(symbol, start_date, end_date, interval)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _fetch_yahoo_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str,
    ) -> pd.DataFrame:
        """
        Fetch data from Yahoo Finance.
        """
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")

        df = yf.download(
            symbol,
            start=start_str,
            end=end_str,
            interval=interval,
            progress=False,
        )

        if df is None or df.empty:
            return pd.DataFrame()

        # Flatten MultiIndex columns returned by newer yfinance versions
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0].lower() for col in df.columns]
        else:
            df.columns = [str(col).lower() for col in df.columns]

        # Ensure required columns exist
        required_columns = ["open", "high", "low", "close", "volume"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        return df[required_columns]  # type: ignore[no-any-return]