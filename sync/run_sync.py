import pandas as pd
import MetaTrader5 as mt5
from pathlib import Path
from datetime import datetime

def sync_account_data():
    from_date=datetime(2020,1,1)
    to_date=datetime.now()

    closed_positions = mt5.history_orders_get(from_date, to_date)
    open_positions = mt5.positions_get()


    _save_closed_position_data(closed_positions)
    _save_open_position_data(open_positions)

    pass


def _save_closed_position_data(closed_positions: list):
    columns = [
        "ticket",
        "symbol",
        "type",
        "volume_initial",
        "price_open",
        "sl",
        "tp",
    ]

    if closed_positions:
        df = pd.DataFrame([position._asdict() for position in closed_positions])

        df = df[columns]
    else:
        df = pd.DataFrame(columns=columns)

    _save_data(df, 'closed_positions')


def _save_open_position_data(open_positions: list):
    columns = [
        "ticket",
        "symbol",
        "type",
        "volume",
        "price_open",
        "sl",
        "tp",
    ]

    if open_positions:
        df = pd.DataFrame([position._asdict() for position in open_positions])

        df = df[columns]
    else:
        df = pd.DataFrame(columns=columns)
        
    _save_data(df, 'open_positions')


def _save_data(data: pd.DataFrame, keyname: str):
    output_dir = Path("data/")
    output_dir.mkdir(parents=True, exist_ok=True)


    filename = f"{keyname}.csv"
    output_path = output_dir / filename


    data.to_csv(output_path, index=False)

    print(f"Saved {len(data)} {keyname} to {output_path}")
