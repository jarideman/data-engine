from fastapi import APIRouter
from positions.open_positions import get_open_positions
from positions.closed_positions import get_closed_positions
from account.account_info import get_account_info

router = APIRouter()


@router.get("/api/positions/open")
def open_positions():
    return get_open_positions()


@router.get("/api/positions/closed")
def closed_positions():
    return get_closed_positions()


@router.get("/api/account")
def account_info():
    return get_account_info()
