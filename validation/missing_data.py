from pathlib import Path


def check_missing_data():
    data_dir = Path("data/")
    history_orders_file = data_dir / "history_orders.csv"
    open_positions_file = data_dir / "open_positions.csv"

    if not history_orders_file.exists():
        return False
    
    if not open_positions_file.exists():
        return False

    return True