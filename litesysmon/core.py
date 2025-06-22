
import os
import psutil
import argparse
import time
import logging
import csv
import configparser
from tabulate import tabulate
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from .process_grouping import group_processes_by_type
from .resource_graph import plot_resource_usage

CONFIG_FILE = 'config.ini'
LOG_FILE = 'litesysmon.log'
CSV_FILE = 'processes.csv'
DEFAULT_CPU_THRESHOLD = 80
DEFAULT_MEM_THRESHOLD = 80

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

console = Console()

def load_config():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config['THRESHOLDS'] = {
            'cpu_threshold': str(DEFAULT_CPU_THRESHOLD),
            'mem_threshold': str(DEFAULT_MEM_THRESHOLD)
        }
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
    config.read(CONFIG_FILE)
    cpu = int(config['THRESHOLDS']['cpu_threshold'])
    mem = int(config['THRESHOLDS']['mem_threshold'])
    return cpu, mem

def save_config(cpu, mem):
    config = configparser.ConfigParser()
    config['THRESHOLDS'] = {
        'cpu_threshold': str(cpu),
        'mem_threshold': str(mem)
    }
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)

def parse_args():
    cpu_help = f"Set CPU usage threshold for alerts (default: {DEFAULT_CPU_THRESHOLD}%%)"
    mem_help = f"Set memory usage threshold for alerts (default: {DEFAULT_MEM_THRESHOLD}%%)"

    parser = argparse.ArgumentParser(
        prog='litesysmon',
        description='LiteSysMon — A lightweight Linux system process monitor.',
        epilog='Example: litesysmon --sort cpu --filter python --alert --log'
    )

    parser.add_argument('--sort', choices=['cpu', 'memory'], help='Sort processes by CPU or memory usage')
    parser.add_argument('--filter', metavar='NAME', help='Filter processes by name')
    parser.add_argument('--interval', metavar='SECONDS', type=int, default=1, help='Refresh interval (default: 1)')
    parser.add_argument('--log', action='store_true', help='Enable logging to litesysmon.log')
    parser.add_argument('--version', action='store_true', help='Show the version of LiteSysMon')
    parser.add_argument('--export', action='store_true', help='Export process stats to CSV')
    parser.add_argument('--alert', action='store_true', help='Enable CPU/memory usage alerts')
    parser.add_argument('--cpu-threshold', type=int, help=cpu_help)
    parser.add_argument('--mem-threshold', type=int, help=mem_help)
    parser.add_argument('--tui', action='store_true', help='Run in interactive terminal dashboard mode')
    return parser.parse_args()

def fetch_processes():
    return list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']))

def display_processes(processes):
    data = [[p.info['pid'], p.info['name'], f"{p.info['cpu_percent']:.1f}%", f"{p.info['memory_percent']:.1f}%"]
            for p in processes]
    table = tabulate(data, headers=["PID", "Name", "CPU", "Memory"], tablefmt="grid")
    console.print(table)

def check_thresholds(processes, cpu_threshold, mem_threshold):
    for p in processes:
        cpu = p.info['cpu_percent']
        mem = p.info['memory_percent']
        if cpu > cpu_threshold:
            console.print(f"[bold red]Alert:[/] {p.info['name']} (PID {p.info['pid']}) CPU {cpu:.1f}%")
        if mem > mem_threshold:
            console.print(f"[bold red]Alert:[/] {p.info['name']} (PID {p.info['pid']}) Memory {mem:.1f}%")

def log_top_processes(processes, top_n=5):
    for p in processes[:top_n]:
        logging.info(f"PID {p.info['pid']} {p.info['name']} CPU {p.info['cpu_percent']}% MEM {p.info['memory_percent']}%")

def export_to_csv(processes):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["PID", "Name", "CPU", "Memory"])
        for p in processes:
            writer.writerow([p.info['pid'], p.info['name'],
                            f"{p.info['cpu_percent']:.1f}%", f"{p.info['memory_percent']:.1f}%"])
    console.print(f"[green]Exported to {CSV_FILE}[/]")

def show_version():
    console.print(Panel.fit("[bold cyan]LiteSysMon v1.0.0 — Lightweight Linux System Monitor[/]"))

def run_tui(interval, cpu_threshold, mem_threshold):
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="top", ratio=3),
        Layout(name="bottom", ratio=2)
    )
    layout["top"].split_row(
        Layout(name="processes"),
        Layout(name="system")
    )
    layout["bottom"].split_row(
        Layout(name="alerts"),
        Layout(name="summary")
    )

    def render():
        procs = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']),
                       key=lambda p: p.info['cpu_percent'], reverse=True)
        table = Table(title="Top Processes", expand=True)
        table.add_column("PID", style="cyan", justify="right")
        table.add_column("Name", style="magenta")
        table.add_column("CPU %", justify="right")
        table.add_column("MEM %", justify="right")

        alerts = []
        for p in procs[:10]:
            try:
                cpu = p.info['cpu_percent']
                mem = p.info['memory_percent']
                table.add_row(str(p.info['pid']), p.info['name'], f"{cpu:.1f}", f"{mem:.1f}")
                if cpu > cpu_threshold:
                    alerts.append(f"[red]⚠ {p.info['name']} CPU: {cpu:.1f}%[/]")
                if mem > mem_threshold:
                    alerts.append(f"[red]⚠ {p.info['name']} MEM: {mem:.1f}%[/]")
            except:
                continue

        layout["header"].update(Panel(Text("LiteSysMon Dashboard (TUI Mode)", justify="center", style="bold white on blue")))
        layout["processes"].update(table)

        sysinfo = f"CPU Usage: {psutil.cpu_percent()}%\nMemory Usage: {psutil.virtual_memory().percent}%"
        layout["system"].update(Panel(sysinfo, title="System Info", border_style="green"))

        layout["alerts"].update(Panel("\n".join(alerts) or "No alerts", title="Alerts", border_style="red"))
        
        user, system = 0, 0
        for p in procs:
            try:
                if p.username() == 'root':
                    system += 1
                else:
                    user += 1
            except:
                continue
        summary_text = f"User Processes: {user}\nSystem Processes: {system}\nTotal: {len(procs)}"
        layout["summary"].update(Panel(summary_text, title="Process Summary", border_style="blue"))

        return layout

    with Live(render(), refresh_per_second=1, screen=True):
        while True:
            time.sleep(interval)

def main():
    args = parse_args()

    if args.version:
        show_version()
        return

    cpu_threshold, mem_threshold = load_config()
    if args.cpu_threshold:
        cpu_threshold = args.cpu_threshold
    if args.mem_threshold:
        mem_threshold = args.mem_threshold
    save_config(cpu_threshold, mem_threshold)

    if args.tui:
        run_tui(args.interval, cpu_threshold, mem_threshold)
        return

    while True:
        processes = fetch_processes()
        for p in processes:
            p.cpu_percent()
        time.sleep(0.1)
        for p in processes:
            p.cpu_percent()

        if args.filter:
            processes = [p for p in processes if args.filter.lower() in p.info['name'].lower()]

        if args.sort:
            processes.sort(key=lambda p: p.info[f'{args.sort}_percent'], reverse=True)

        os.system('clear')
        show_version()
        display_processes(processes)

        if args.log:
            log_top_processes(processes)

        if args.alert:
            check_thresholds(processes, cpu_threshold, mem_threshold)

        if args.export:
            export_to_csv(processes)

        time.sleep(args.interval)
