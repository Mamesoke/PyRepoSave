# 🛡️ Automatic Save Backup

Python script to automatically and manually back up `.save` files from a game.

## Features

- Automatic backup every 10 minutes
- Manual backup using F5 and F6
- Compresses .save files into .zip format
- Stores everything in the Backups folder

## ⚙️ Setup

1. Create and activate a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv .venv
# Activate it (Windows)
.venv\Scripts\activate
# Activate it (macOS/Linux)
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

Just run the script:
```bash
python main.py
```

## Commands
- Press F5 to trigger a manual backup
- Press F6 to restore the latest backup
- Press F7 to pause automatic backups
- Press F8 to resume automatic backups
