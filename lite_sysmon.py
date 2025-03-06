import psutil
import argparse

def list_processes(sort_by="cpu", filter_by=None):
    """Lists running processes with sorting and filtering."""
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

    # Print process list
    for proc in processes:
        print(f"{proc['pid']:<10}{proc['name']:<25}{proc['cpu_percent']:<10}{proc['memory_percent']:<10}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LiteSysMon - A Lightweight System Monitor")
    parser.add_argument("--sort", choices=["cpu", "memory"], default="cpu", help="Sort processes by CPU or memory usage")
    parser.add_argument("--filter", help="Filter processes by name")
    args = parser.parse_args()

    list_processes(sort_by=args.sort, filter_by=args.filter)
