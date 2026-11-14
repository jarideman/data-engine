import MetaTrader5 as mt5
from datetime import datetime, time, timezone
from collections import defaultdict


def _format_account_info(account_info):
  return {
    'login': account_info.login,
    'name': account_info.name,
    'leverage': account_info.leverage,
    'balance': account_info.balance,
    'equity': account_info.equity,
    'profit': account_info.profit,
    'server': account_info.server,
    'trade_allowed': account_info.trade_allowed,
    'trade_expert': account_info.trade_expert,
  }


def get_account_info():
  account_info = mt5.account_info()

  return _format_account_info(account_info)


def get_portfolio_details():
        # Get account information
        account = mt5.account_info()

        if account is None:
            raise Exception(
                f"Unable to retrieve account information: {mt5.last_error()}"
            )
        
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
        account = mt5.account_info()

        if account is None:
            raise Exception(
                f"Unable to retrieve account information: {mt5.last_error()}"
            )

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

        # Only include positions that have been fully closed.
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

        # Estimate starting balance by reversing all historical
        # deal movements from the current account balance.
        total_historical_movements = sum(
            get_deal_net_profit(deal)
            for deal in deals
        )

        deposits = 0.0
        withdrawals = 0.0

        # Collect all historical cash movements
        cash_movements = []

        if deals:
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
        all_movements.sort(key=lambda item: (item[0], item[1]))

        # Calculate drawdown
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

            # Percentage relative to peak
            drawdown_percent = (
                (drawdown / peak_balance) * 100
                if peak_balance > 0
                else 0.0
            )

            if drawdown > maximum_drawdown:
                maximum_drawdown = drawdown
                maximum_drawdown_percent = drawdown_percent

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
                "value": f"{profit_factor:.2f} %"
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


def get_performance_data():
  return [
    {
      "date": "Mar 22",
      "Balance": 1050,
      "P&L": 50,
    },
    {
      "date": "Mar 23",
      "Balance": 1095,
      "P&L": 95,
    },
    {
      "date": "Mar 24",
      "Balance": 1025,
      "P&L": 25,
    },
    {
      "date": "Mar 25",
      "Balance": 1035,
      "P&L": 35,
    },
    {
      "date": "Mar 26",
      "Balance": 1060,
      "P&L": 60,
    },
  ];