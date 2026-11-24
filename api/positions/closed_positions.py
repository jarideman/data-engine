import MetaTrader5 as mt5
from datetime import datetime, timezone
from collections import defaultdict
from shared.net_profit import get_deal_net_profit


# Check/refactor this code
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
                "ticket": deal.ticket,
                "symbol": deal.symbol,
                "position_id": position_id,
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
    now = datetime.now(timezone.utc)

    from_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    to_date = datetime.fromtimestamp(now, tz=timezone.utc)

    # TODO: Ombouwen naar positions
    history_deals = mt5.history_deals_get(from_date, to_date)

    if history_deals is None:
        return None

    return _format_positions(history_deals)


def get_closed_position(ticket: int):
    # TODO: Ombouwen naar positions
    deals = mt5.history_deals_get(ticket=ticket)

    if deals is None or len(deals) == 0:
        return None

    return _format_positions(deals)[0]
