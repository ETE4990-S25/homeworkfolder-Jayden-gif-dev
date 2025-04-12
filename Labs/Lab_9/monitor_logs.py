import time
import threading
from analyze_logs_monitor import start_monitor, start_visualizer  # I moved monitor/graph code into a separate helper file

# I made this a generator because it felt cleaner than writing a giant if-else
def menu_options():
    yield "1", "Text Summary (CRITICAL alerts)", start_monitor
    yield "2", "Live Graph (Matplotlib)", start_visualizer
    yield "q", "Quit", None

def main():
    print("=== Log Summary Monitor ===")

    # Instead of writing a bunch of ifs, I just convert the generator to a dictionary
    options = {key: (desc, action) for key, desc, action in menu_options()}

    # Show the menu to the user
    for key, (desc, _) in options.items():
        print(f"{key}. {desc}")

    # This lets me type like " 1 " or "Q" without crashing
    choice = input("Choose an option: ").strip().lower()

    if choice not in options:
        print("Invalid choice. Exiting.")
        return

    desc, action = options[choice]

    if choice == 'q':
        print("Goodbye.")
        return

    # Once a valid choice is made, I call the action (either monitor or graph)
    print(f"Starting: {desc}...\n")
    action()

    # This used to run forever but I like this better — I just press ENTER to stop
    try:
        input("Press ENTER to stop monitoring...\n")
        print("Stopping...")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")

# This is just the usual Python entry point
if __name__ == "__main__":
    main()
