from connection import init_mt5
from pathlib import Path
from dotenv import load_dotenv
from database import start_connection


BASE_DIR = Path(__file__).resolve().parent
API_DIR = BASE_DIR / "api"


def main():
    if not init_mt5():
        return

    load_dotenv()

    start_connection()


if __name__ == "__main__":
    main()
