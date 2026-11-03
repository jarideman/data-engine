
import MetaTrader5 as mt5


def get_trading_data():
        account = mt5.account_info()

        if account is None:
            raise Exception("Account information unavailable")

        balance = account.balance
        equity = account.equity

        positions = mt5.positions_get()

        if positions is None:
            raise Exception(f"Positions error: {mt5.last_error()}")

        # Group positions by symbol
        grouped = {}

        for pos in positions:

            symbol = pos.symbol
            symbol_info = mt5.symbol_info(symbol)

            if symbol_info is None:
                continue

            if symbol not in grouped:
                grouped[symbol] = {
                    "symbol": symbol,
                    "value": 0,
                    "volume": 0,
                    "profit": 0,
                    "margin": 0,
                    "positions_count": 0
                }

            position_value = (
                pos.volume *
                symbol_info.trade_contract_size *
                pos.price_current
            )

            order_type = (
                mt5.ORDER_TYPE_BUY
                if pos.type == mt5.POSITION_TYPE_BUY
                else mt5.ORDER_TYPE_SELL
            )

            margin = mt5.order_calc_margin(
                order_type,
                symbol,
                pos.volume,
                pos.price_current
            )

            grouped[symbol]["value"] += position_value
            grouped[symbol]["volume"] += pos.volume
            grouped[symbol]["profit"] += pos.profit
            grouped[symbol]["margin"] += margin or 0
            grouped[symbol]["positions_count"] += 1

        allocation = []
        total_exposure = 0

        for symbol, item in grouped.items():
            total_exposure += item["value"]

            allocation.append({
                "name": symbol,
                "value": round(
                    item["value"] / balance * 100 if balance else 0, 2
                ),
            })

        # Cash as remaining nominal balance
        cash = max(0, balance - total_exposure)

        allocation.append({
            "name": "Cash",
            "value": round(
                cash / balance * 100 if balance else 0, 2
            ),
        })

        return allocation
