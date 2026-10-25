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
