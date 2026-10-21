import MetaTrader5 as mt5

def _format_positions(positions):
    result = []

    if positions is None:
        return result

    for position in positions:
        result.append({
            "price_open": position.price_open,
            "sl": position.sl,
            "tp": position.tp,
            "symbol": position.symbol,
            "profit": position.profit,
        })

    return result


def get_open_positions():
    open_positions = mt5.positions_get()

    return _format_positions(open_positions)
