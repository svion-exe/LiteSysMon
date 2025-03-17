import psutil
import time
import argparse
import json
import pandas as pd

def list_processes():
    """List all running processes with PID, Name, and Memory Usage."""
    processes = []
    print(f"{'PID':<10} {'Name':<25} {'Memory Usage (MB)':<20}")
    print("=" * 60)

    for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info']):
        info = proc.info
        mem_usage_mb = info['memory_info'].rss / (1024 * 1024)
        processes.append({"PID": info['pid'], "Name": info['name'], "Memory Usage (MB)": mem_usage_mb})
        print(f"{info['pid']:<10} {info['name']:<25} {mem_usage_mb:<20.2f}")

    return processes

def export_processes(processes, file_format, output_file):
    """Export process data to CSV or JSON."""
    if file_format == "json":
        with open(output_file, "w") as f:
            json.dump(processes, f, indent=4)
        print(f"✅ Process data exported to {output_file} (JSON format)")
    elif file_format == "csv":
        df = pd.DataFrame(processes)
        df.to_csv(output_file, index=False)
        print(f"✅ Process data exported to {output_file} (CSV format)")
    else:
        print("❌ Unsupported file format! Use 'csv' or 'json'.")

def monitor_processes(interval):
    """Continuously monitor processes at a given interval."""
    try:
        while True:
            print("\n🔍 Updating process list...\n")
            list_processes()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LiteSysMon - A Lightweight System Process Monitor")
    parser.add_argument("--monitor", action="store_true", help="Enable real-time monitoring mode")
    parser.add_argument("--interval", type=int, default=5, help="Monitoring interval in seconds")
    parser.add_argument("--export", choices=["csv", "json"], help="Export process data format (csv/json)")
    parser.add_argument("--output", type=str, help="Output file name")

    args = parser.parse_args()

    processes = list_processes()

    if args.export and args.output:
        export_processes(processes, args.export, args.output)

    if args.monitor:
        monitor_processes(args.interval)
