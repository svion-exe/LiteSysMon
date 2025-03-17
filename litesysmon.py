import psutil
import time
import argparse

def list_processes():
    """List all running processes with PID, Name, and Memory Usage."""
    print(f"{'PID':<10} {'Name':<25} {'Memory Usage (MB)':<20}")
    print("="*60)
    
    for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info']):
        info = proc.info
        print(f"{info['pid']:<10} {info['name']:<25} {info['memory_info'].rss / (1024 * 1024):<20.2f}")

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

    args = parser.parse_args()

    if args.monitor:
        monitor_processes(args.interval)
    else:
        list_processes()
