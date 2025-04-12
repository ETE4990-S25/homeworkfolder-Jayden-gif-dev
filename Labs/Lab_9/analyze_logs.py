import os
import re
import json
from collections import defaultdict
from structured_logger import sample_formatter  # using the custom formatter I wrote earlier

# Use this from project 1 to read the log file
# I had to change the import path a bit to match my folder structure
def read_log_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return []
    except Exception as e:
        print(f"Couldn't read the file: {e}")
        return []

def parse_log_line(line):
    # This took from jupyter notebook to get the regex right
    # I had to tweak the regex a bit to match the log format from sample_formatter
    pattern = r"^(\d{2}/\d{2} \d{2}:\d{2}:\d{2})\s+(\w+)\s+:(.+?):\s+(.*)$"
    match = re.match(pattern, line)
    if match:
        timestamp, level, name, message = match.groups()
        return {
            "timestamp": timestamp.strip(),
            "level": level.strip(),
            "name": name.strip(),
            "message": message.strip()
        }
    return None

# I replaced the old split/slice parser with one that uses the new regex parser above.
def parse_log_lines(log_lines):
    parsed_logs = []
    for line in log_lines:
        entry = parse_log_line(line)
        if entry:
            parsed_logs.append(entry)
    return parsed_logs

# This function counts the occurrences of each log level and message, and returns a summary.
# Took a while to get this right — was originally trying to do this with a list of tuples.
def count_log_levels(parsed_logs):
    summary = defaultdict(lambda: defaultdict(int))
    for entry in parsed_logs:
        level = entry['level']
        msg = entry['message']
        summary[level][msg] += 1
    return summary

def main():
    # This part is just to make sure the log file is in the right place
    # I had to change the path a bit to match my folder structure
    log_input_path = os.path.join("Labs", "Lab_9", "Logs", "RSVP_Agent_processing.log")
    log_output_path = os.path.join("Labs", "Lab_9", "Logs", "log_summary.json")
    print(f"Trying to read the log file from: {log_input_path}")
    lines = read_log_file(log_input_path)
    print(f"Going through {len(lines)} lines...")
    parsed = parse_log_lines(lines)
    print("Counting up the log levels and messages...")
    summary = count_log_levels(parsed)
    # This part gave me some headaches until I realized the folder had to exist
    os.makedirs("Labs/Lab_9/Logs", exist_ok=True)
    print("Checking the full path just to be sure:")
    print("   ", os.path.abspath(log_input_path))
    print(f"Saving everything to: {log_output_path}")
    with open(log_output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4)

    print("Done! Should be good to go.")

if __name__ == "__main__":
    main()
