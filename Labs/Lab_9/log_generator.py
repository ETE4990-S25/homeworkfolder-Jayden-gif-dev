import logging
import os
from datetime import datetime

# I wanted my logs to match the format from the RSVP Agent,
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