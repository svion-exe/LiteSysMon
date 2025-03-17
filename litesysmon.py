import psutil

def list_processes():
    print(f"{'PID':<10} {'Name':<25} {'Memory Usage (MB)':<20}")
    print("="*60)
    
    for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info']):
        info = proc.info
        print(f"{info['pid']:<10} {info['name']:<25} {info['memory_info'].rss / (1024 * 1024):<20.2f}")

if __name__ == "__main__":
    list_processes()
