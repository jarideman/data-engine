import pandas as pd
from pathlib import Path


def sync_account_data():
    # TODO: define what can be saved and whats needed live.
    # _save_data(data, 'file_name')

    pass


def _save_data(data: pd.DataFrame, keyname: str):
    output_dir = Path("data/")
    output_dir.mkdir(parents=True, exist_ok=True)


    filename = f"{keyname}.csv"
    output_path = output_dir / filename


    data.to_csv(output_path, index=False)

    print(f"Saved {len(data)} {keyname} to {output_path}")
