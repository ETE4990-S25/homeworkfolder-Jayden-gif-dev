import logging
import os
from datetime import datetime

# I wanted my logs to match the format from the RSVP Agent file,
# so I created this custom formatter class.
class sample_formatter(logging.Formatter):
    def format(self, record):
        # I format the timestamp to look like MM/DD HH:MM:SS
        timestamp = datetime.fromtimestamp(record.created).strftime("%m/%d %H:%M:%S")

        # I pad the log level to 7 characters so everything lines up nicely
        level = record.levelname.ljust(7)

        # This part shows the logger name (which includes the component and function)
        source = f":{record.name}:"

        # I return everything as one structured log line
        return f"{timestamp} {level}: {source} {record.getMessage()}"

# I made this class to manage logs for each component in a clean way
class structured_logger:
    def __init__(self, component_name, function_name):
        # These are just the names for organization
        self.component_name = component_name
        self.function_name = function_name

        # This is where I create the actual logger with a unique name
        self.logger = logging.getLogger(f"{component_name}:{function_name}")
        self.logger.setLevel(logging.DEBUG)

        # This method sets up the file and formatter — I wanted to keep it modular
        self._setup_handler()

    def _setup_handler(self):
        # I make sure the logs directory exists before writing
        os.makedirs("logs", exist_ok=True)

        # Each component has its own log file
        log_file_path = f"logs/{self.component_name}.log"

        # I only want to add a handler if it hasn’t been added already
        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_file_path)
            formatter = sample_formatter()
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    # This method is what I actually use to write logs
    def log(self, level, message):
        # I dynamically get the logging method based on level (e.g. info, warning, etc.)
        log_method = getattr(self.logger, level.lower(), None)
        if log_method:
            log_method(message)
