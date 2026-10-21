import MetaTrader5 as mt5
from datetime import datetime, timezone

def _format_positions(positions):
    result = []

    if positions is None:
        return result

    for position in positions:
        result.append({
            "price_open": position.price,
            "lot_size": position.volume,
            "profit": position.profit,
            "symbol": position.symbol
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

    #deze kunnen wel gewoon offline?   + optie tot force sync / check metatraerd webhooks
    history_deals = mt5.history_deals_get(from_date, to_date)

    if history_deals is None:
        return []

    # Keep only completed historical orders
    closed_position = [
        order for order in history_deals
        if order.entry in [mt5.DEAL_ENTRY_OUT,
            mt5.DEAL_ENTRY_OUT_BY,
            mt5.DEAL_ENTRY_INOUT]
    ]

    return _format_positions(closed_position)
