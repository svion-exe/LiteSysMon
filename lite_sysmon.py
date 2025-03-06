import psutil
import argparse
import logging
import os
import platform
from datetime import datetime

# Determine OS-specific log directory
if platform.system() == "Windows":
    LOG_DIR = os.path.join(os.getenv("APPDATA"), "LiteSysMon_Logs")  # Use AppData for logs
else:
    LOG_DIR = "logs"

# Create log directory if not exists
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
log_filename = os.path.join(LOG_DIR, "sysmon.log")
logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s - %(message)s")

def list_processes(sort_by="cpu", filter_by=None, log=False, alert_cpu=None, alert_memory=None):
    """Lists running processes with sorting, filtering, logging, and alerts for high resource usage."""
    processes = []
    alerts = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            proc_info = proc.info
            if filter_by and filter_by.lower() not in proc_info['name'].lower():
                continue  # Skip if process name does not match filter
            processes.append(proc_info)

            # Check for high CPU usage alert
            if alert_cpu and proc_info['cpu_percent'] >= alert_cpu:
                alerts.append(f"⚠️ High CPU Usage: {proc_info['name']} (PID {proc_info['pid']}) is using {proc_info['cpu_percent']}% CPU")

            # Check for high memory usage alert
            if alert_memory and proc_info['memory_percent'] >= alert_memory:
                alerts.append(f"⚠️ High Memory Usage: {proc_info['name']} (PID {proc_info['pid']}) is using {proc_info['memory_percent']}% Memory")

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

    # Print alerts
    if alerts:
        print("\n🔴 ALERTS:")
        for alert in alerts:
            print(alert)

    # Save to log file if logging is enabled
    if log:
        logging.info("\n".join(log_entries))
        if alerts:
            logging.warning("\n".join(alerts))
        print(f"\n[INFO] Process details logged to {log_filename}")

def main():
    parser = argparse.ArgumentParser(description="LiteSysMon - A Lightweight System Monitor")
    parser.add_argument("--sort", choices=["cpu", "memory"], default="cpu", help="Sort processes by CPU or memory usage")
    parser.add_argument("--filter", help="Filter processes by name")
    parser.add_argument("--log", action="store_true", help="Enable logging of process data")
    parser.add_argument("--alert-cpu", type=float, help="Set CPU usage alert threshold (in %)")
    parser.add_argument("--alert-memory", type=float, help="Set memory usage alert threshold (in %)")
    args = parser.parse_args()

    list_processes(sort_by=args.sort, filter_by=args.filter, log=args.log,
                   alert_cpu=args.alert_cpu, alert_memory=args.alert_memory)

if __name__ == "__main__":
    main()
