from fastapi import APIRouter
from account.account_info import get_account_info, get_portfolio_details, get_risk_details, get_performance_data
from dashboard.allocations import get_trading_data


router = APIRouter(
    prefix="/account",
    tags=["Account"]
)


@router.get("/info")
def account_info():
    return get_account_info()


@router.get("/portfolio")
def portfolio_details():
    return get_portfolio_details()


@router.get("/risk")
def risk_details():
    return get_risk_details()


@router.get("/performance")
def performance_data():
    return get_performance_data()


@router.get("/allocations")
def allocations():
    return get_trading_data()
