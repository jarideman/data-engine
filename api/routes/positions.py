from fastapi import APIRouter
from positions.open_positions import get_open_positions, get_open_position
from positions.closed_positions import get_closed_positions, get_closed_position


router = APIRouter(
    prefix="/positions",
    tags=["Positions"]
)


@router.get("/open")
def open_positions():
    return get_open_positions()


@router.get("/open/{ticket}")
def open_positions(ticket: int):
    return get_open_position(ticket=ticket)


@router.get("/closed")
def closed_positions():
    return get_closed_positions()


@router.get("/closed/{ticket}")
def closed_position(ticket: int):
    return get_closed_position(ticket=ticket)
