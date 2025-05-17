import random
from datetime import datetime
import threading

from utils import get_date_range, chunk_dates
from downloader import get_data

# Taken from template but modified
rates = ["EUR", "GBP", "USD", "DZD", "AUD", "BWP", "BND", "CAD", "CLP", "CNY", "COP", "CZK", "DKK", "HUF", "ISK", "INR", "IDR", "ILS", "KZT", "KRW", "KWD", "LYD", "MYR", "MUR", "NPR", "NZD", "NOK", "OMR", "PKR", "PLN", "QAR", "RUB", "SAR", "SGD", "ZAR", "LKR", "SEK", "CHF", "THB", "TTD"]
rates_for_base = [r for r in rates if r != "USD" and r != "EUR" and r != "GBP"]

start_date = datetime.strptime("2011-05-04", "%Y-%m-%d")
end_date = datetime.today()
max_threads = 15 # Number of threads to use increase a little bit

def threaded_ally(date_chunk, base):
    for date_str in date_chunk:
        get_data(date_str, base)

def main():
    base_currency = random.choice(rates_for_base)
    print(f"Base: {base_currency}")

    all_dates = get_date_range(start_date, end_date)
    chunks = chunk_dates(all_dates, max_threads)
    threads = []

    for chunk in chunks:
        t = threading.Thread(target=threaded_ally, args=(chunk, base_currency))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Done.")

if __name__ == "__main__":
    main()
