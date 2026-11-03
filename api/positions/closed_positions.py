import MetaTrader5 as mt5
from datetime import datetime, timezone
from collections import defaultdict

# Check/reformat this code
def _format_positions(deals):
    result = []

    if not deals:
        return result

    positions = defaultdict(list)

    for deal in deals:
        positions[deal.position_id].append(deal)

    for position_id, position_deals in positions.items():
        opening_deals = [
            d for d in position_deals
            if d.entry == mt5.DEAL_ENTRY_IN
        ]

        closing_deals = [
            d for d in position_deals
            if d.entry in (
                mt5.DEAL_ENTRY_OUT,
                mt5.DEAL_ENTRY_OUT_BY,
                mt5.DEAL_ENTRY_INOUT
            )
        ]

        if not closing_deals:
            continue

        total_open_volume = sum(d.volume for d in opening_deals)

        if total_open_volume:
            price_open = sum(
                d.price * d.volume for d in opening_deals
            ) / total_open_volume
        else:
            price_open = None

        for deal in closing_deals:
            order_type = (
                "buy"
                if deal.type == mt5.DEAL_TYPE_SELL
                else "sell"
            )

            close_time = datetime.fromtimestamp(
                deal.time,
                tz=timezone.utc
            )

            result.append({
                "symbol": deal.symbol,
                "position_id": position_id,
                "status": "closed",
                "type": order_type,
                "volume": deal.volume,
                "price_open": price_open,
                "price_exit": deal.price,
                "profit": deal.profit + deal.swap + deal.commission,
                "date": close_time.strftime("%Y-%m-%d %H:%M:%S"),
            })

    return result


def get_closed_positions():
    symbol = "EURUSD"

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        raise RuntimeError(
            f"Cannot retrieve tick for {symbol}: {mt5.last_error()}"
        )

    from_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    to_date = datetime.fromtimestamp(tick.time, tz=timezone.utc)

    history_deals = mt5.history_deals_get(from_date, to_date)

    if history_deals is None:
        raise RuntimeError(
            f"Cannot retrieve history: {mt5.last_error()}"
        )

    return _format_positions(history_deals)
