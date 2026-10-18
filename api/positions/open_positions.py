import pandas as pd
import os
from pathlib import Path


def get_open_positions():
    df = pd.read_csv(Path(os.getenv("BASE_DIR")) / "data/open_positions.csv")

    return df["ticket"].tolist()
