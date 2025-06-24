# LiteSysMon 🖥️⚡

**LiteSysMon** is a lightweight, terminal-based Linux system process monitor built in Python. It displays real-time CPU and memory usage, supports smart alerts, logs stats, exports to CSV, and even visualizes usage with graphs.

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux-orange.svg)](https://www.linux.org/)

![LiteSysMon Demo](https://via.placeholder.com/800x400/1a1a1a/00ff00?text=LiteSysMon+Terminal+Dashboard)

---

## 🚀 Features

- 🔍 **Real-time process monitoring** - Live CPU and memory usage tracking
- 📊 **Smart sorting** - Sort by CPU or memory usage  
- 🔎 **Process filtering** - Filter processes by name pattern
- 🚨 **Intelligent alerts** - Configurable CPU/memory threshold alerts
- 🧠 **Persistent configuration** - Settings saved via CLI or config.ini
- 📁 **CSV export** - Export process statistics for analysis
- 📈 **Resource visualization** - Plot usage graphs with matplotlib
- 📚 **Comprehensive logging** - Historical analysis with log files
- 🎨 **Rich TUI mode** - Beautiful terminal dashboard with live updates
- ⚙️ **Process grouping** - Categorize by user/system/daemon processes

---

## 📦 Installation

### Option 1: Install from Source (Recommended)
```bash
# Clone the repository
git clone https://github.com/svion-exe/LiteSysMon.git
cd LiteSysMon

# Install dependencies
pip install -r requirements.txt

# Install LiteSysMon
pip install .
```

### Option 2: Development Installation
```bash
git clone https://github.com/svion-exe/LiteSysMon.git
cd LiteSysMon
pip install -e .
```

### Option 3: Direct Dependency Installation
```bash
pip install psutil tabulate matplotlib rich
# Then install LiteSysMon using Option 1
```

---

## 🎯 Quick Start

After installation, LiteSysMon is available as a global command:

```bash
# Basic process monitoring
litesysmon

# Interactive dashboard mode (Recommended!)
litesysmon --tui

# Sort processes by CPU usage with alerts
litesysmon --sort cpu --alert

# Filter Python processes and export to CSV
litesysmon --filter python --export --log

# Custom thresholds and refresh interval
litesysmon --cpu-threshold 90 --mem-threshold 85 --interval 2
```

---

## 📋 Command Line Options

```bash
Usage: litesysmon [OPTIONS]

Options:
  --sort {cpu,memory}     Sort processes by CPU or memory usage
  --filter NAME           Filter processes by name pattern
  --interval SECONDS      Refresh interval in seconds (default: 1)
  --log                   Enable logging to litesysmon.log
  --export                Export process statistics to CSV
  --alert                 Enable CPU/memory usage alerts
  --cpu-threshold INT     CPU usage alert threshold (default: 80%)
  --mem-threshold INT     Memory usage alert threshold (default: 80%)
  --tui                   Run interactive terminal dashboard mode
  --version               Show LiteSysMon version
  --help                  Show this help message

Examples:
  litesysmon --sort cpu --filter python --alert --log
  litesysmon --tui --cpu-threshold 75 --interval 0.5
  litesysmon --export --mem-threshold 90
```

---

## 🎨 TUI Dashboard Mode

Launch the beautiful terminal dashboard:

```bash
litesysmon --tui
```

**Dashboard Features:**
- 📊 Live process table with top CPU consumers
- 📈 Real-time system CPU and memory statistics  
- 🚨 Alert panel showing threshold violations
- 📋 Process summary with user/system breakdown
- 🎯 Auto-refreshing every second
- 🌈 Color-coded alerts and status indicators

---

## ⚙️ Configuration

LiteSysMon automatically creates a `config.ini` file for persistent settings:

```ini
[THRESHOLDS]
cpu_threshold = 80
mem_threshold = 80
```

**Configuration Methods:**
1. **CLI Arguments:** `--cpu-threshold 90 --mem-threshold 85`
2. **Config File:** Edit `config.ini` directly
3. **Auto-save:** CLI arguments automatically update config.ini

---

## 📁 Output Files

| File | Description |
|------|-------------|
| `litesysmon.log` | Process monitoring logs (with `--log`) |
| `processes.csv` | Process statistics export (with `--export`) |
| `resource_usage.png` | Resource usage graphs |
| `config.ini` | Persistent configuration settings |

---

## 🔧 Requirements

- **Python:** 3.6 or higher
- **Operating System:** Linux/Unix systems
- **Dependencies:**
  - `psutil` >= 5.8.0 - System and process utilities
  - `tabulate` >= 0.8.9 - Table formatting
  - `matplotlib` >= 3.3.0 - Graph plotting
  - `rich` >= 10.0.0 - Terminal formatting and TUI

---

## 🌟 Usage Examples

### Basic Monitoring
```bash
# Monitor all processes
litesysmon

# Monitor with 2-second refresh rate
litesysmon --interval 2
```

### Advanced Filtering & Sorting
```bash
# Show only Python processes, sorted by memory
litesysmon --filter python --sort memory

# Monitor Chrome processes with alerts
litesysmon --filter chrome --alert --cpu-threshold 70
```

### Data Export & Logging
```bash
# Log top processes and export to CSV
litesysmon --log --export --sort cpu

# Monitor with custom thresholds and logging
litesysmon --alert --cpu-threshold 85 --mem-threshold 90 --log
```

### Dashboard Mode
```bash
# Launch interactive dashboard
litesysmon --tui

# Dashboard with custom settings
litesysmon --tui --cpu-threshold 75 --interval 0.5
```

---

## 🏗️ Project Structure

```
LiteSysMon/
├── litesysmon/
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── core.py              # Main application logic
│   ├── process_grouping.py  # Process categorization
│   └── resource_graph.py    # Visualization utilities
├── build/                   # Build artifacts
├── litesysmon.egg-info/     # Package metadata
├── config.ini               # Configuration file
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
├── pyproject.toml           # Build configuration
├── README.md                # This file
└── .gitignore               # Git ignore rules
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
git clone https://github.com/svion-exee/LiteSysMon.git
cd LiteSysMon
pip install -e .  # Editable installation
```

---

## 🐛 Troubleshooting

### Common Issues

**Permission Errors:**
```bash
pip install --user .
```

**Python Command Not Found:**
```bash
python3 -m pip install .
```

**Dependency Installation Issues:**
```bash
# Install dependencies separately
pip install psutil tabulate matplotlib rich
pip install .
```

**TUI Mode Not Working:**
- Ensure terminal supports colors and Unicode
- Try resizing terminal window
- Check Rich library installation

---

## 📊 Performance

LiteSysMon is designed to be lightweight:
- **Memory footprint:** ~10-15MB
- **CPU usage:** <1% on modern systems
- **Startup time:** <2 seconds
- **Refresh rate:** Configurable (default: 1 second)

---

## 🛣️ Roadmap

- [ ] 📧 Email alert notifications
- [ ] 🌐 Web dashboard interface  
- [ ] 📱 Mobile app companion
- [ ] 🐳 Docker container support
- [ ] 📊 Historical data analysis
- [ ] 🔌 Plugin system
- [ ] 🌍 Multi-language support

---




## 👨‍💻 Author

**Rajat Singh Rawat** ([@svion-exe](https://github.com/svion-exe))

- 🐙 GitHub: [svion-exe](https://github.com/svion-exe)
- 📧 Email: [your.email@example.com](mailto:rajatsinghr16@gmail.com)

---

## 🙏 Acknowledgments

- **psutil** - Cross-platform system and process utilities
- **Rich** - Beautiful terminal formatting library
- **matplotlib** - Comprehensive plotting library
- **tabulate** - Pretty-print tabular data

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

[![GitHub stars](https://img.shields.io/github/stars/svion-exe/LiteSysMon.svg?style=social&label=Star)](https://github.com/svion-exe/LiteSysMon)
[![GitHub forks](https://img.shields.io/github/forks/svion-exe/LiteSysMon.svg?style=social&label=Fork)](https://github.com/svion-exe/LiteSysMon/fork)

---

<div align="center">
  <p>Made with ❤️ and ☕ by <a href="https://github.com/svion-exe">@svion-exe</a></p>
  <p><strong>LiteSysMon</strong> - Monitoring made simple!</p>
</div>
