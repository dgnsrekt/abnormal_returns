from datetime import datetime, timedelta, date


def get_year_and_month():
    now = datetime.now()
    today = now.date()
    year = today.year
    month = today.month
    return year, month
