import MetaTrader5 as mt5
from datetime import datetime, time, timezone, timedelta
from collections import defaultdict
from shared.date_filter import get_filter_start_date


def _account_info():
  account = mt5.account_info()

  if account is None:
    raise Exception(
      f"Unable to retrieve account information: {mt5.last_error()}"
  )

  return account


def get_account_info():
  account = _account_info()

  return {
    'login': account.login,
    'name': account.name,
    'leverage': account.leverage,
    'balance': account.balance,
    'equity': account.equity,
    'profit': account.profit,
    'server': account.server,
    'trade_allowed': account.trade_allowed,
    'trade_expert': account.trade_expert,
  }


def get_portfolio_details():
    account = _account_info()

    deals = mt5.history_deals_get(
        datetime(2000, 1, 1, tzinfo=timezone.utc),
        datetime.now(timezone.utc)
    )

    deposits = 0.0
    withdrawals = 0.0

    if deals:
        for deal in deals:
            if deal.type == mt5.DEAL_TYPE_BALANCE:
                if deal.profit > 0:
                    deposits += deal.profit
                elif deal.profit < 0:
                    withdrawals += abs(deal.profit)

    net_deposits = deposits - withdrawals

    balance = account.balance
    equity = account.equity
    floating_pnl = account.profit

    # Realized P&L = balance minus net deposits
    realized_pnl = balance - net_deposits

    # Total P&L = realized P&L + floating P&L
    total_pnl = realized_pnl + floating_pnl

    # Total return percentage
    total_return = (
        (total_pnl / net_deposits) * 100
        if net_deposits > 0
        else 0.0
    )

    today_start = datetime.combine(
        datetime.now(timezone.utc).date(),
        time.min,
        tzinfo=timezone.utc
    )

    today_deals = mt5.history_deals_get(
        today_start,
        datetime.now(timezone.utc)
    )

    today_profit = 0.0

    if today_deals:
        for deal in today_deals:
            if deal.type in (
                mt5.DEAL_TYPE_BUY,
                mt5.DEAL_TYPE_SELL
            ):
                today_profit += (
                    deal.profit
                    + deal.swap
                    + deal.commission
                    + deal.fee
                )

    return [
        {
            "label": "Total Portfolio Value",
            "value": round(equity, 2)
        },
        {
            "label": "Total P&L",
            "value": round(total_pnl, 2)
        },
        {
            "label": "Total Return (%)",
            "value": f"{total_return:.2f} %"
        },
        {
            "label": "Floating P&L",
            "value": round(floating_pnl, 2)
        },
        {
            "label": "Today's P&L",
            "value": round(today_profit, 2)
        },
        {
            "label": "Cash Balance",
            "value": round(balance, 2)
        }
    ]


def get_risk_details():
    account = _account_info()

    deals = mt5.history_deals_get(
        datetime(2000, 1, 1, tzinfo=timezone.utc),
        datetime.now(timezone.utc)
    )

    if deals is None:
        raise Exception(
            f"Unable to retrieve trading history: {mt5.last_error()}"
        )

    positions = mt5.positions_get()

    if positions is None:
        positions = []

    # Calculate floating PnL from open positions
    floating_pnl = sum(
        position.profit + position.swap
        for position in positions
    )

    open_position_ids = {
        position.identifier for position in positions
    }

    trades = defaultdict(float)

    def get_deal_net_profit(deal):
        return (
            deal.profit
            + deal.swap
            + deal.commission
            + getattr(deal, "fee", 0.0)
        )

    trading_deals = []

    for deal in deals:

        if deal.type not in (
            mt5.DEAL_TYPE_BUY,
            mt5.DEAL_TYPE_SELL
        ):
            continue

        position_id = deal.position_id

        if position_id == 0:
            continue

        net_profit = get_deal_net_profit(deal)

        trades[position_id] += net_profit
        trading_deals.append((deal, net_profit))

    # Only include positions that have been fully closed
    closed_trades = [
        profit
        for position_id, profit in trades.items()
        if position_id not in open_position_ids
    ]

    winning_trades = [
        profit for profit in closed_trades
        if profit > 0
    ]

    losing_trades = [
        profit for profit in closed_trades
        if profit < 0
    ]

    total_trades = len(closed_trades)
    total_wins = len(winning_trades)
    total_losses = len(losing_trades)

    # Win Rate
    win_rate = (
        (total_wins / total_trades) * 100
        if total_trades > 0
        else 0.0
    )

    # Profit Factor
    gross_profit = sum(winning_trades)
    gross_loss = abs(sum(losing_trades))

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0
        else 0.0
    )

    # Average Win
    average_win = (
        gross_profit / total_wins
        if total_wins > 0
        else 0.0
    )

    # Average Loss (negative value)
    average_loss = (
        sum(losing_trades) / total_losses
        if total_losses > 0
        else 0.0
    )

    # Calculate historical deposits and withdrawals
    deposits = 0.0
    withdrawals = 0.0

    cash_movements = []

    for deal in deals:

        if deal.type == mt5.DEAL_TYPE_BALANCE:

            amount = deal.profit

            if amount > 0:
                deposits += amount

            elif amount < 0:
                withdrawals += abs(amount)

            cash_movements.append(
                (deal.time, deal.ticket, amount)
            )

    net_deposits = deposits - withdrawals

    # Calculate total historical trading result
    total_trading_profit = sum(
        net_profit for deal, net_profit in trading_deals
    )

    # Reconstruct original balance
    initial_balance = (
        account.balance
        - net_deposits
        - total_trading_profit
    )

    # Combine trading deals and cash movements
    all_movements = []

    for deal, net_profit in trading_deals:
        all_movements.append(
            (deal.time, deal.ticket, net_profit)
        )

    all_movements.extend(cash_movements)

    # Sort chronologically
    all_movements.sort(
        key=lambda item: (item[0], item[1])
    )

    # Calculate historical drawdown
    running_balance = initial_balance
    peak_balance = initial_balance

    maximum_drawdown = 0.0
    maximum_drawdown_percent = 0.0

    for timestamp, ticket, movement in all_movements:

        running_balance += movement

        # Update peak
        if running_balance > peak_balance:
            peak_balance = running_balance

        # Calculate drawdown
        drawdown = peak_balance - running_balance

        drawdown_percent = (
            (drawdown / peak_balance) * 100
            if peak_balance > 0
            else 0.0
        )

        if drawdown > maximum_drawdown:
            maximum_drawdown = drawdown
            maximum_drawdown_percent = drawdown_percent


    # MT5 equity includes floating PnL and other
    # account-level adjustments.
    current_equity = account.equity

    current_drawdown = peak_balance - current_equity

    current_drawdown_percent = (
        (current_drawdown / peak_balance) * 100
        if peak_balance > 0
        else 0.0
    )

    if current_drawdown > maximum_drawdown:
        maximum_drawdown = current_drawdown
        maximum_drawdown_percent = current_drawdown_percent

    return [
        {
            "label": "Maximum Drawdown",
            "value": round(-maximum_drawdown, 2),
        },
        {
            "label": "Maximum Drawdown (%)",
            "value": f"{-maximum_drawdown_percent:.2f} %"
        },
        {
            "label": "Win Rate",
            "value": f"{win_rate:.2f} %"
        },
        {
            "label": "Profit Factor",
            "value": f"{profit_factor:.2f}"
        },
        {
            "label": "Average Win",
            "value": round(average_win, 2)
        },
        {
            "label": "Average Loss",
            "value": round(average_loss, 2)
        }
    ]


def get_performance_data(time_filter="ALL"):
    account = _account_info()

    now = datetime.now(timezone.utc)

    start_date = get_filter_start_date(time_filter)

    deals = mt5.history_deals_get(
        datetime(2000, 1, 1, tzinfo=timezone.utc),
        now
    )

    if deals is None:
        raise Exception(
            f"Unable to retrieve trading history: {mt5.last_error()}"
        )

    def get_deal_net_profit(deal):
        return (
            deal.profit
            + deal.swap
            + deal.commission
            + getattr(deal, "fee", 0.0)
        )


    daily_trading = defaultdict(float)
    daily_cash_movements = defaultdict(float)

    all_movements = []

    total_historical_movements = 0.0

    for deal in deals:
        deal_date = datetime.fromtimestamp(
            deal.time,
            tz=timezone.utc
        ).date()

        if deal.type in (
            mt5.DEAL_TYPE_BUY,
            mt5.DEAL_TYPE_SELL
        ):

            net_profit = get_deal_net_profit(deal)

            total_historical_movements += net_profit

            daily_trading[deal_date] += net_profit

            all_movements.append((
                deal.time,
                deal.ticket,
                net_profit,
                deal_date,
                "trading"
            ))

        elif deal.type == mt5.DEAL_TYPE_BALANCE:

            amount = deal.profit

            total_historical_movements += amount

            daily_cash_movements[deal_date] += amount

            all_movements.append((
                deal.time,
                deal.ticket,
                amount,
                deal_date,
                "cash"
            ))


    initial_balance = (
        account.balance - total_historical_movements
    )

    # Sort movements chronologically
    all_movements.sort(
        key=lambda item: (item[0], item[1])
    )

    running_balance = initial_balance

    first_active_date = None

    if initial_balance != 0 and all_movements:
        first_active_date = datetime.fromtimestamp(
            all_movements[0][0],
            tz=timezone.utc
        ).date()

    for timestamp, ticket, movement, deal_date, movement_type in all_movements:

        running_balance += movement

        if running_balance != 0 and first_active_date is None:
            first_active_date = deal_date

    if first_active_date is None:
        return []


    effective_start_date = max(
        start_date.date(),
        first_active_date
    )

    end_date = now.date()


    start_balance = initial_balance

    for timestamp, ticket, movement, deal_date, movement_type in all_movements:

        if deal_date < effective_start_date:
            start_balance += movement


    cumulative_pnl = sum(
        movement
        for timestamp, ticket, movement, deal_date, movement_type in all_movements
        if (
            deal_date >= first_active_date
            and deal_date < effective_start_date
            and movement_type == "trading"
        )
    )


    performance_data = []

    running_balance = start_balance

    current_date = effective_start_date

    while current_date <= end_date:

        trading_pnl = daily_trading.get(current_date, 0.0)

        cash_movement = daily_cash_movements.get(
            current_date, 0.0
        )

        running_balance += trading_pnl + cash_movement

        # Lifetime P&L, not selected-period P&L
        cumulative_pnl += trading_pnl

        performance_data.append({
            "date": current_date.strftime("%b %d"),
            "Balance": round(running_balance, 2),
            "P&L": round(cumulative_pnl, 2),
        })

        current_date += timedelta(days=1)


    positions = mt5.positions_get()

    if positions is None:
        positions = []

    floating_pnl = sum(
        position.profit + position.swap
        for position in positions
    )

    if performance_data:

        # Current equity includes floating P&L
        performance_data[-1]["Balance"] = round(
            account.equity,
            2
        )

        # Lifetime P&L + current floating P&L
        performance_data[-1]["P&L"] = round(
            cumulative_pnl + floating_pnl,
            2
        )

    return performance_data


def get_allocations():
    account = _account_info()

    balance = account.balance

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
