import psutil
import argparse
import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
log_filename = os.path.join(LOG_DIR, "sysmon.log")
logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s - %(message)s")

def list_processes(sort_by="cpu", filter_by=None, log=False):
    """Lists running processes with sorting, filtering, and optional logging."""
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            proc_info = proc.info
            if filter_by and filter_by.lower() not in proc_info['name'].lower():
                continue  # Skip if process name does not match filter
            processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Sorting logic
    if sort_by == "cpu":
        processes.sort(key=lambda p: p['cpu_percent'], reverse=True)
    elif sort_by == "memory":
        processes.sort(key=lambda p: p['memory_percent'], reverse=True)

    # Print header
    print(f"{'PID':<10}{'Process Name':<25}{'CPU %':<10}{'Memory %':<10}")
    print("=" * 55)

    log_entries = []
    for proc in processes:
        entry = f"{proc['pid']:<10}{proc['name']:<25}{proc['cpu_percent']:<10}{proc['memory_percent']:<10}"
        print(entry)
        log_entries.append(entry)

    # Save to log file if logging is enabled
    if log:
        logging.info("\n".join(log_entries))
        print("\n[INFO] Process details logged to logs/sysmon.log")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LiteSysMon - A Lightweight System Monitor")
    parser.add_argument("--sort", choices=["cpu", "memory"], default="cpu", help="Sort processes by CPU or memory usage")
    parser.add_argument("--filter", help="Filter processes by name")
    parser.add_argument("--log", action="store_true", help="Enable logging of process data")
    args = parser.parse_args()

    list_processes(sort_by=args.sort, filter_by=args.filter, log=args.log)
