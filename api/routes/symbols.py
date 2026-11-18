from fastapi import APIRouter, Query
from symbol.symbol_data import get_symbol_data


router = APIRouter(
    prefix="/symbols",
    tags=["Symbols"]
)


@router.get("/{symbol}")
def symbol(
    symbol: str,
    filter: str = Query(
        default="ALL",
        pattern="^(1D|1W|1M|3M|6M|YTD|1Y|ALL)$"
    )
):
    return get_symbol_data(symbol, filter)

