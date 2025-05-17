import requests
import xmltodict
import json
import os
import logging
from time import sleep
from datetime import datetime
from utils import ensure_dir, get_date_range, chunk_dates

# Setup logger
logging.basicConfig(
    filename="exchange_scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Taken from template but modified to use some retries, and print ok/fail messages
def get_data(date, base, retries=2, delay=1):
    url = f"https://www.floatrates.com/historical-exchange-rates.html?operation=rates&pb_id=1775&page=historical&currency_date={date}&base_currency_code={base}&format_type=xml"

    folder = ensure_dir(base)
    json_path = os.path.join(folder, f"{date}_exchange_rates_{base}.json")
    xml_path = os.path.join(folder, f"{date}_exchange_rates_{base}.xml")

    if os.path.exists(json_path) and os.path.exists(xml_path):
        logging.warning(f"Skipped: {base} on {date} — file already exists.")
        return

    for attempt in range(retries + 1):
        try:
            logging.info(f"Attempting: {base} on {date} (Attempt {attempt+1})")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Save raw XML
            with open(xml_path, "w", encoding="utf-8") as xml_file:
                xml_file.write(response.text)
            logging.info(f"Saved XML: {xml_path}")

            # Parse XML and save JSON
            data_dict = xmltodict.parse(response.text)
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(data_dict, json_file, indent=4)
            logging.info(f"Saved JSON: {json_path}")

            return  # success, exit loop

        except Exception as e:
            logging.error(f"Error on {base} at {date} (Attempt {attempt+1}): {e}")
            sleep(delay)

    logging.error(f"Failed after retries: {base} on {date}")
