from fastapi import APIRouter, Query
from account.account_info import get_account_info, get_portfolio_details, get_risk_details, get_performance_data, get_allocations


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
def performance_data(
    filter: str = Query(
        default="ALL",
        pattern="^(1D|1W|1M|3M|6M|YTD|1Y|ALL)$"
    )
):
    return get_performance_data(filter)


@router.get("/allocations")
def allocations():
    return get_allocations()
