import os
from datetime import datetime, timedelta
from math import ceil

def ensure_dir(base_currency):
    path = os.path.join("data", base_currency)
    os.makedirs(path, exist_ok=True)
    return path

def get_date_range(start_date, end_date):
    days = (end_date - start_date).days
    return [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days + 1)]

def chunk_dates(dates, n_chunks):
    chunk_size = ceil(len(dates) / n_chunks)
    return [dates[i:i + chunk_size] for i in range(0, len(dates), chunk_size)]
