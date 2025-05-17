import time
import threading
from downloader import get_data
from datetime import datetime, timedelta

# Test config
base = "KWD"
start = datetime.strptime("2011-05-04", "%Y-%m-%d")
days_to_test = 10
dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days_to_test)]

# Sequential execution
def run_sequential():
    for date in dates:
        get_data(date, base)

# Parallel execution using threads
def run_parallel(max_threads=10):
    threads = []
    for date in dates:
        t = threading.Thread(target=get_data, args=(date, base))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# Benchmarking
print("Benchmarking Sequential Execution...")
start_time = time.time()
run_sequential()
seq_duration = time.time() - start_time
print(f"Sequential time: {seq_duration:.2f} seconds\n")

print("Benchmarking Parallel Execution...")
start_time = time.time()
run_parallel()
par_duration = time.time() - start_time
print(f"Parallel time: {par_duration:.2f} seconds\n")

# Comparison
improvement = ((seq_duration - par_duration) / seq_duration) * 100
print(f"Parallel download was {improvement:.1f}% faster than sequential.")
