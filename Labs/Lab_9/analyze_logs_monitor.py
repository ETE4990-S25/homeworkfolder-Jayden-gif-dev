import json
import time
import threading
from collections import defaultdict
import matplotlib.pyplot as plt
import os

# I had issues with file paths at first — this just makes sure it works no matter where I run the script from
base_dir = os.path.dirname(os.path.abspath(__file__))
log_summary_path = os.path.join(base_dir, "Logs", "log_summary.json")

# I use this to remember the previous state of the log
last_snapshot = {}

# This function just keeps checking the log file and prints stuff when something new happens
def monitor_log_summary():
    global last_snapshot

    while True:
        try:
            with open(log_summary_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Making a copy of what's in the log right now
            new_snapshot = defaultdict(dict)
            for level, messages in data.items():
                for msg, count in messages.items():
                    new_snapshot[level][msg] = count

            # Only show stuff if it changed since last time
            if new_snapshot != last_snapshot:
                print("\n--- Updated Log Summary ---")
                for level in new_snapshot:
                    total = sum(new_snapshot[level].values())
                    print(f"{level}: {total} entries")

                    # I only really care about CRITICAL messages for now
                    if level == "CRITICAL":
                        for msg, count in new_snapshot[level].items():
                            # Show it if it's a new critical message
                            if msg not in last_snapshot.get("CRITICAL", {}):
                                print(f"[CRITICAL] {msg} (x{count})")

                # Save what we just saw so we can compare it next time
                last_snapshot = new_snapshot

        except FileNotFoundError:
            print("[Monitor] File not found... still waiting for it to show up.")
        except json.JSONDecodeError:
            print("[Monitor] JSON error — probably still writing or got corrupted.")
        time.sleep(3)  # just chill for a few seconds before checking again


# This just shows the log data as a bar chart that updates
def visualize_log_levels():
    plt.ion()  # this makes the chart live and auto-refresh
    fig, ax = plt.subplots()

    while True:
        try:
            with open(log_summary_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            levels = list(data.keys())
            counts = [sum(data[level].values()) for level in levels]

            # Refresh the chart — it just wipes and redraws
            ax.clear()
            ax.bar(levels, counts)
            ax.set_title("Log Level Distribution")
            ax.set_xlabel("Log Level")
            ax.set_ylabel("Total Messages")
            plt.draw()
            plt.pause(2)  # wait a bit before checking again

        except Exception as e:
            print(f"[Graph] Error: {e}")
            time.sleep(2)


# This gets called when I press 1 in the menu (monitor_logs.py)
def start_monitor():
    monitor_thread = threading.Thread(target=monitor_log_summary, daemon=True)
    monitor_thread.start()
    print("Log monitor started.")  # Just a confirmation


# This one is for the graph (option 2 in monitor_logs.py)
def start_visualizer():
    visualize_thread = threading.Thread(target=visualize_log_levels, daemon=True)
    visualize_thread.start()
    print("Visualizer started.")  # Another confirmation
