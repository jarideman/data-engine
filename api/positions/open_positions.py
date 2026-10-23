import MetaTrader5 as mt5
from datetime import datetime, timezone


def _format_positions(positions):
    result = []

    if positions is None:
        return result

    for position in positions:
        order_type = "buy" if position.type == mt5.POSITION_TYPE_BUY else "sell"

        open_time = datetime.fromtimestamp(
            position.time, tz=timezone.utc
        )
        date = open_time.strftime("%Y-%m-%d %H:%M:%S")

        result.append({
            "symbol": position.symbol,
            "status": 'open',
            "type": order_type,
            'volume': position.volume,
            'price_open': position.price_open,
            'price_current': position.price_current,
            'stop_loss': position.sl,
            'take_profit': position.tp,
            'profit': position.profit,
            'date': date,
        })

    return result


def get_open_positions():
    open_positions = mt5.positions_get()

    return _format_positions(open_positions)
