import psutil

def list_processes():
    """Lists all running processes with PID, name, CPU, and memory usage."""
    print(f"{'PID':<10}{'Process Name':<25}{'CPU %':<10}{'Memory %':<10}")
    print("=" * 55)

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            print(f"{proc.info['pid']:<10}{proc.info['name']:<25}{proc.info['cpu_percent']:<10}{proc.info['memory_percent']:<10}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

if __name__ == "__main__":
    list_processes()
