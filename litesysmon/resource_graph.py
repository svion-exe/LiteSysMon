import matplotlib.pyplot as plt
import psutil
import time

def plot_resource_usage(duration=10, interval=1):
    timestamps = []
    cpu_usages = []
    mem_usages = []

    for _ in range(int(duration / interval)):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        timestamps.append(time.strftime("%H:%M:%S"))
        cpu_usages.append(cpu)
        mem_usages.append(mem)
        time.sleep(interval)

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, cpu_usages, label='CPU %')
    plt.plot(timestamps, mem_usages, label='Memory %')
    plt.xlabel('Time')
    plt.ylabel('Usage (%)')
    plt.title('System Resource Usage')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid()
    plt.savefig('resource_usage.png')
    plt.show()
