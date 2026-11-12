import MetaTrader5 as mt5

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
  return [
    {
      "label": "Total Portfolio Value",
      "value": 0,
    },
    {
      "label": "Total P&L",
      "value": 0,
    },
    {
      "label": "Total Return (%)",
      "value": 0,
    },
    {
      "label": "Today's P&L",
      "value": 0,
    },
    {
      "label": "Cash Balance",
      "value": 0,
    },
  ]


def get_risk_details():
  return [
    {
      "label": "Maximum Drawdown",
      "value": 0,
    },
    {
      "label": "Win Rate",
      "value": 0,
    },
    {
      "label": "Profit Factor",
      "value": 0,
    },
    {
      "label": "Average Win",
      "value": 0,
    },
    {
      "label": "Average Loss",
      "value": 0,
    },
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