import cProfile
import pstats
from downloader import get_data
from datetime import datetime, timedelta

def run_download():
    base = "KWD"
    start = datetime.strptime("2011-05-04", "%Y-%m-%d")
    end = start + timedelta(days=10)  # profile just 10 days

    for i in range((end - start).days + 1):
        date = (start + timedelta(days=i)).strftime("%Y-%m-%d")
        get_data(date, base)

# Start profiling
cProfile.run('run_download()', 'download_profile.stats')
p = pstats.Stats('download_profile.stats')
p.sort_stats('tottime').print_stats(20)
