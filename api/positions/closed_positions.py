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

        # TODO: Fill remaining data
        result.append({
            "symbol": position.symbol,
            "status": 'closed',
            "type": order_type,
            'volume': position.volume,
            'price_open': position.price,
            'price_exit': '',
            'stop_loss': '',
            'take_profit': '',
            'profit': position.profit,
            'date': date, 
        })

    return result


def get_closed_positions():
    symbol = "EURUSD"

    tick = mt5.symbol_info_tick(symbol)

    if tick is not None:
        server_time = datetime.fromtimestamp(
            tick.time,
            tz=timezone.utc
        )
    
    from_date = datetime(2024, 1, 1)
    to_date = server_time

    # TODO: Check if this can be cached
    history_deals = mt5.history_deals_get(from_date, to_date)

    if history_deals is None:
        return []

    closed_position = [
        order for order in history_deals
        if order.entry in [mt5.DEAL_ENTRY_OUT,
            mt5.DEAL_ENTRY_OUT_BY,
            mt5.DEAL_ENTRY_INOUT]
    ]

    return _format_positions(closed_position)
