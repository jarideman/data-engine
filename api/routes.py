from fastapi import APIRouter
from positions.open_positions import get_open_positions
from positions.closed_positions import get_closed_positions
from account.account_info import get_account_info, get_portfolio_details, get_risk_details, get_performance_data
from dashboard.allocations import get_trading_data

router = APIRouter()


@router.get("/api/positions/open")
def open_positions():
    return get_open_positions()


@router.get("/api/positions/closed")
def closed_positions():
    return get_closed_positions()


@router.get("/api/account/info")
def account_info():
    return get_account_info()


@router.get("/api/account/portfolio")
def portfolio_details():
    return get_portfolio_details()


@router.get("/api/account/risk")
def risk_details():
    return get_risk_details()


@router.get("/api/account/performance")
def performance_data():
    return get_performance_data()


@router.get("/api/account/allocations")
def allocations():
    return get_trading_data()
