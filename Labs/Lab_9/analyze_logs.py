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


def parse_log_lines(log_lines):
    parsed_logs = []
# This regex is a bit of a mess but it works for now. I might clean it up later.
# I had to change the regex a bit to match the log format
    for line in log_lines:
        if len(line.strip()) < 20:
            continue
        timestamp = line[:17].strip()
        remainder = line[17:].strip()
        if ':' not in remainder:
            continue
        level_part, rest = remainder.split(':', 1)
        level = level_part.strip()
        if ':' not in rest:
            continue
        name_part, message = rest.split(':', 1)
        name = name_part.strip()
        message = message.strip()
        parsed_logs.append({
            "timestamp": timestamp,
            "level": level,
            "name": name,
            "message": message
        })
    return parsed_logs

# This function counts the occurrences of each log level and message, and returns a summary. Took a while to get this right
# because I was trying to use a list of tuples instead of a dictionary. This way is much cleaner.
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
