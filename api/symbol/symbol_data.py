import MetaTrader5 as mt5
from datetime import datetime, timezone
from shared.date_filter import get_filter_start_date, get_timeframe
from shared.now import get_now


def get_symbol_data(symbol: str, time_filter="ALL"):
  start_date = get_filter_start_date(time_filter)
  timeframe = get_timeframe(time_filter)

  symbol_info = mt5.symbol_info(symbol)

  if symbol_info is None:
    raise Exception(f"Symbol {symbol} not found")

  now = get_now()

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

  symbol_data = []

  for rate in rates:
    candle_date = datetime.fromtimestamp(
      rate["time"],
      tz=timezone.utc
    )

    symbol_data.append({
      "date": candle_date.strftime("%b %d %H:%M"),
      "open": round(float(rate["open"]), 5),
      "high": round(float(rate["high"]), 5),
      "low": round(float(rate["low"]), 5),
      "close": round(float(rate["close"]), 5),
    })

  return symbol_data
