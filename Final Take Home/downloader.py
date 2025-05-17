import requests
import xmltodict
import json
import os
import time
from utils import ensure_dir, get_date_range, chunk_dates

# Taken from template but modified to use some retries, and print ok/fail messages
def get_data(date, base, retries=2):
    url = f"https://www.floatrates.com/historical-exchange-rates.html?operation=rates&pb_id=1775&page=historical&currency_date={date}&base_currency_code={base}&format_type=xml"
    folder = ensure_dir(base)
    json_path = os.path.join(folder, f"{date}_exchange_rates_{base}.json")
    xml_path = os.path.join(folder, f"{date}_exchange_rates_{base}.xml")

    if os.path.exists(json_path) and os.path.exists(xml_path):
        print(f"Skipped: {date}")
        return
    # I added a retry loop in case something times out or fails
    for attempt in range(retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            # Save raw XML
            with open(xml_path, "w", encoding="utf-8") as xml_file:
                xml_file.write(response.text)
            # Convert XML and save as JSON    
            data_dict = xmltodict.parse(response.text)
            with open(json_path, "w") as json_file:
                json.dump(data_dict, json_file, indent=4)
            print(f"Saved: {date}")
            return
        except Exception as e:
            print(f"Retry {attempt+1}: {date}")

    print(f"Failed: {date}")
