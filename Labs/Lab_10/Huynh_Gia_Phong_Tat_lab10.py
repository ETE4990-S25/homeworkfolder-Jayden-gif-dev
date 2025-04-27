import docker
import time
import threading
import logging
import logging.handlers
import os

# Initialize Docker client
client = docker.from_env()
containers = ["adminer", "mysql"]

# Setup logging folder
if not os.path.exists("logs"):
    os.makedirs("logs")

# System logger for general container status, restarts, and errors
# This is somewhat from our notes.
system_logger = logging.getLogger("LoggingSetup")
system_logger.setLevel(logging.INFO)

system_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
system_file_handler = logging.handlers.TimedRotatingFileHandler(
    filename="logs/system.log",
    when="D",
    backupCount=5
)
# Create a file handler for system logs with rotation (Somewhat from our notes)
system_file_handler.setFormatter(system_formatter)
system_logger.addHandler(system_file_handler)

# Create a separate logger for each container
def setup_container_logger(container_name):
    logger = logging.getLogger(f"{container_name}_logger")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s | %(message)s")
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=f"logs/{container_name}.log",
        when="D",
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

# Small helper for consistent console prints, this is from our notes when I was doing the logging setup
def friendly_print(msg):
    print(f"{time.strftime('%H:%M:%S')} | {msg}")

# Monitor container health and handle auto-restarts
def start_shutdown_check():
    threading.current_thread().name = "ContainerMonitor"

    while True:
        time.sleep(10)
        friendly_print("Checking containers...")
        
        for container_name in containers:
            try:
                container = client.containers.get(container_name)
                container.reload()

                if container.status != "running":
                    container.start()
                    system_logger.info(f"Container '{container_name}' restarted after stop.")
                    friendly_print(f"Started '{container_name}'.")

                if time.strftime("%H") == "01":
                    container.restart()
                    system_logger.info(f"Container '{container_name}' scheduled 1AM restart.")
                    friendly_print(f"Restarted '{container_name}' at 1AM.")

            except Exception as e:
                system_logger.error(f"Error handling '{container_name}': {e}")
                friendly_print(f"Issue detected with '{container_name}'. See logs.")

# Continuously stream logs for a container
def stream_container_logs(container_name):
    threading.current_thread().name = f"LogStreamer-{container_name}"
    container_logger = setup_container_logger(container_name)

    while True:
        try:
            container = client.containers.get(container_name)
            logs = container.logs(stream=True, follow=True)
            friendly_print(f"Streaming logs for '{container_name}'...")

            for line in logs:
                decoded_line = line.decode('utf-8').strip()
                message = f"[{container_name}] {decoded_line}"
                print(message)
                container_logger.info(decoded_line)

        except Exception as e:
            system_logger.error(f"Failed log streaming for '{container_name}': {e}")
            friendly_print(f"Retrying log stream for '{container_name}' in 5s...")
            time.sleep(5)

# Startup: monitor containers + start log streamers
if __name__ == "__main__":
    friendly_print("Starting logging setup and container monitoring...")

    shutdown_thread = threading.Thread(target=start_shutdown_check, daemon=True)
    shutdown_thread.start()

    log_threads = []
    for container_name in containers:
        t = threading.Thread(target=stream_container_logs, args=(container_name,), daemon=True)
        t.start()
        log_threads.append(t)

    shutdown_thread.join()
    for t in log_threads:
        t.join()

# References:
# Basically I went through these resources to get the code working .......
# 1. Docker SDK for Python (https://docker-py.readthedocs.io/en/stable/)
#    - Used to control containers: start, restart, fetch logs, reload status.
# 
# 2. Python Logging Module (https://docs.python.org/3/howto/logging.html)
#    - Setup structured logging, separate system and container logs.
#
# 3. TimedRotatingFileHandler (https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler)
#    - Log file rotation daily, keep a history of backups.
# 
# 4. Python Threading Module (https://docs.python.org/3/library/threading.html)
#    - Used to create background threads for health monitoring and log streaming.
#
# 5. Docker Best Practices for Monitoring (https://www.docker.com/blog/monitoring-docker-container-logs/)
#    - Inspired container restart patterns and log streaming models.
#
# 6. Real Python - Logging in Threads (https://realpython.com/python-logging/#logging-in-multiple-threads)
#    - Ensured thread-safe logging and resilience if errors occur inside threads.
