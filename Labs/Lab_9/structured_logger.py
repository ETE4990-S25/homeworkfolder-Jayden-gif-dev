import logging
import os
from datetime import datetime

# Trying to match the RSVP Agent log format
# Starting with a custom formatter class
class sample_formatter(logging.Formatter):
    def format(self, record):
        # Format the timestamp as MM/DD HH:MM:SS
        timestamp = datetime.fromtimestamp(record.created).strftime("%m/%d %H:%M:%S")
        # Pad the log level so it's always aligned
        level = record.levelname.ljust(7)
        # Build the source field with the logger name
        source = f":{record.name}:"
        # Combine all pieces into the final log line
        return f"{timestamp} {level}: {source} {record.getMessage()}"


# Creating a structured logger that uses the formatter above
class structured_logger:

    def __init__(self, component_name, function_name):
        # Passing in the component and function names, just going to hold onto these for now
        self.component_name = component_name
        self.function_name = function_name
        # Logger name needs to be unique, using both names here to make it work
        self.logger = logging.getLogger(f"{component_name}:{function_name}")

        # Going with DEBUG for now, I think that gives me all the log levels
        self.logger.setLevel(logging.DEBUG)
        # Had to separate this into its own method to keep things cleaner
        self._setup_handler()


    def _setup_handler(self):
        # Needed a folder to hold the logs so they don’t end up everywhere
        os.makedirs("Logs", exist_ok=True)

        # One log file per component seemed like the easiest way to organize it
        log_file_path = f"Logs/{self.component_name}.Log"

        # I kept running into duplicate handlers so this check avoids that
        if not self.logger.handlers:
            # This part took a while to figure out — I originally had the path wrong
            file_handler = logging.FileHandler(log_file_path)

            # I finally got the formatter to apply correctly after tweaking this line
            formatter = sample_formatter()
            file_handler.setFormatter(formatter)
            # I remember forgetting to attach this the first time — nothing was logging
            self.logger.addHandler(file_handler)


    def log(self, level, message):
        # Tried a bunch of ways to get the right log method — this one worked best
        log_method = getattr(self.logger, level.lower(), None)
        # Without this check, I was getting errors when passing unknown levels
        if log_method:
            log_method(message)

        # I thought about adding a fallback print but this felt cleaner for now
        