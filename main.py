from connection import init_mt5, deinit_mt5
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent

API_DIR = BASE_DIR / "api"


def main():
    if not init_mt5():
        return

    load_dotenv()


if __name__ == "__main__":
    main()
