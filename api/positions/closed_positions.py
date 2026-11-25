import MetaTrader5 as mt5
from datetime import datetime, timezone
from shared.net_profit import get_deal_net_profit
from shared.now import get_now


def _format_positions(deals):
    if not deals:
        return []

    positions = {}

    for deal in deals:
        position = positions.setdefault(deal.position_id, [0.0, 0.0, []])

        if deal.entry == mt5.DEAL_ENTRY_IN:
            position[0] += deal.price * deal.volume
            position[1] += deal.volume
        elif deal.entry in (
            mt5.DEAL_ENTRY_OUT,
            mt5.DEAL_ENTRY_OUT_BY,
            mt5.DEAL_ENTRY_INOUT,
        ):
            position[2].append(deal)

    result = []

    for position_id, position in positions.items():
        weighted_open_price, total_open_volume, closing_deals = position
        if not closing_deals:
            continue

        price_open = (
            weighted_open_price / total_open_volume
            if total_open_volume
            else None
        )

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
                "ticket": deal.ticket,
                "symbol": deal.symbol,
                "position": position_id,
                "status": "closed",
                "type": order_type,
                "volume": deal.volume,
                "price_open": price_open,
                "price_exit": deal.price,
                "profit": get_deal_net_profit(deal),
                "date": close_time.strftime("%Y-%m-%d %H:%M:%S"),
            })

    return result


def get_closed_positions():
    from_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    to_date = get_now()

    history_deals = mt5.history_deals_get(from_date, to_date)

    if history_deals is None:
        return None

    return _format_positions(history_deals)


def get_closed_position(position: int):
    deals = mt5.history_deals_get(position=position)

    if deals is None or len(deals) == 0:
        return None

    return _format_positions(deals)[0]
