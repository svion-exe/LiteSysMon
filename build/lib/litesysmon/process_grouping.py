import psutil

def group_processes_by_type(processes):
    grouped = {
        'User Processes': [],
        'System Processes': [],
        'Daemon Processes': []
    }

    for proc in processes:
        try:
            username = proc.username()
            if username == 'root':
                grouped['System Processes'].append(proc)
            elif 'daemon' in username or 'dbus' in username:
                grouped['Daemon Processes'].append(proc)
            else:
                grouped['User Processes'].append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return grouped
