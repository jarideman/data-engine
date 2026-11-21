import MetaTrader5 as mt5
from datetime import datetime, timedelta, timezone


def get_filter_start_date(time_filter):
  now = datetime.now(timezone.utc)

  filters = {
    "1D": now - timedelta(days=1),
    "1W": now - timedelta(weeks=1),
    "1M": now - timedelta(days=30),
    "3M": now - timedelta(days=90),
    "6M": now - timedelta(days=180),
    "1Y": now - timedelta(days=365),
    "YTD": datetime(now.year, 1, 1, tzinfo=timezone.utc),
    "ALL": datetime(2000, 1, 1, tzinfo=timezone.utc),
  }

  if time_filter not in filters:
    raise ValueError("Invalid time filter")

  return filters[time_filter]


def get_timeframe(time_filter):
  timeframes = {
    "1D": mt5.TIMEFRAME_H1,
    "1W": mt5.TIMEFRAME_H4,
    "1M": mt5.TIMEFRAME_D1,
    "3M": mt5.TIMEFRAME_D1,
    "6M": mt5.TIMEFRAME_D1,
    "YTD": mt5.TIMEFRAME_W1,
    "1Y": mt5.TIMEFRAME_W1,
    "ALL": mt5.TIMEFRAME_MN1,
  }

  timeframe = timeframes.get(time_filter)

  if timeframe is None:
    raise ValueError(f"Invalid time filter: {time_filter}")

  return timeframe
