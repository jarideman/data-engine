from datetime import datetime, timedelta, timezone


def get_filter_start_date(time_filter):
    now = datetime.now(timezone.utc)

    filters = {
        "1D": now - timedelta(days=1),
        "1W": now - timedelta(weeks=1),
        "1M": now - timedelta(days=30),
        "3M": now - timedelta(days=90),
        "6M": now - timedelta(days=180),
        "1Y": now - timedelta(days=365),
        "YTD": datetime(now.year, 1, 1, tzinfo=timezone.utc),
        "ALL": datetime(2000, 1, 1, tzinfo=timezone.utc),
    }

    if time_filter not in filters:
        raise ValueError("Invalid time filter")

    return filters[time_filter]
