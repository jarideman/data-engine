import pandas as pd
import os
from pathlib import Path


def get_closed_positons():
    df = pd.read_csv(Path(os.getenv("BASE_DIR")) / "data/closed_positions.csv")
    print(df)
    return #get data from csv
