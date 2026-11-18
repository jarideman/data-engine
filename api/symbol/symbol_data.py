import MetaTrader5 as mt5
from datetime import datetime, timezone
from shared.date_filter import get_filter_start_date


def get_symbol_data(symbol: str, time_filter="ALL"):
  now = datetime.now(timezone.utc)

  start_date = get_filter_start_date(time_filter)

  candle_timeframes = {
    "1D": mt5.TIMEFRAME_H1,
    "1W": mt5.TIMEFRAME_H4,
    "1M": mt5.TIMEFRAME_D1,
    "3M": mt5.TIMEFRAME_D1,
    "6M": mt5.TIMEFRAME_D1,
    "YTD": mt5.TIMEFRAME_W1,
    "1Y": mt5.TIMEFRAME_W1,
    "ALL": mt5.TIMEFRAME_MN1,
  }

  timeframe = candle_timeframes.get(time_filter)

  if timeframe is None:
    raise ValueError(f"Invalid time filter: {time_filter}")

  symbol_info = mt5.symbol_info(symbol)

  if symbol_info is None:
    raise Exception(f"Symbol {symbol} not found")

  if not symbol_info.visible:
    if not mt5.symbol_select(symbol, True):
      raise Exception(f"Unable to select symbol {symbol}")

  rates = mt5.copy_rates_range(
    symbol,
    timeframe,
    start_date,
    now
  )

  if rates is None:
    raise Exception(
      f"Unable to retrieve rates: {mt5.last_error()}"
    )

  chart_data = []

  for rate in rates:
    candle_date = datetime.fromtimestamp(
      rate["time"],
      tz=timezone.utc
    )

  chart_data.append({
    "date": candle_date.strftime("%b %d %H:%M"),
    "open": round(float(rate["open"]), 5),
    "high": round(float(rate["high"]), 5),
    "low": round(float(rate["low"]), 5),
    "close": round(float(rate["close"]), 5),
  })

  return chart_data
