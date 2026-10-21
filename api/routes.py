from fastapi import APIRouter
from positions.open_positions import get_open_positions
from positions.closed_positions import get_closed_positions

router = APIRouter()


@router.get("/api/postions/open")
def open_positions():
    return get_open_positions()


@router.get("/api/postions/closed")
def closed_positions():
    return get_closed_positions()
