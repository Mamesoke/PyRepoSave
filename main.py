import os
import zipfile
import shutil
import time
from datetime import datetime
import threading
import keyboard

# Pause/resume flag
paused = False

def get_save_path():
    base = os.getenv("APPDATA")  # This points to Roaming
    roaming = os.path.join(base, "semiwork", "Repo", "saves")
    local_low = os.path.join(base.replace("Roaming", "LocalLow"), "semiwork", "Repo", "saves")

    if os.path.exists(local_low):
        return local_low
    elif os.path.exists(roaming):
        return roaming
    else:
        return None

def create_backup():
    save_path = get_save_path()
    if not save_path:
        print("❌ Saves folder not found.")
        return

    backup_dir = os.path.join(os.getcwd(), "Backups")
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_name = os.path.join(backup_dir, f"backup_{timestamp}.zip")

    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for foldername, _, filenames in os.walk(save_path):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    arcname = os.path.relpath(filepath, save_path)
                    zipf.write(filepath, arcname)

        print(f"✅ Backup created: {zip_name}")
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return

    # Clean old backups (keep only the last 40)
    try:
        backups = [f for f in os.listdir(backup_dir) if f.endswith(".zip")]
        if len(backups) > 40:
            backups_full_path = [os.path.join(backup_dir, f) for f in backups]
            backups_full_path.sort(key=os.path.getctime)
            for old_backup in backups_full_path[:-40]:
                os.remove(old_backup)
                print(f"🗑️ Backup deleted: {old_backup}")
    except Exception as e:
        print(f"⚠️ Error while cleaning old backups: {e}")

def load_last_backup():
    backup_dir = os.path.join(os.getcwd(), "Backups")
    if not os.path.exists(backup_dir):
        print("❌ Backups folder does not exist.")
        return

    backups = [f for f in os.listdir(backup_dir) if f.endswith(".zip")]
    if not backups:
        print("❌ No available backups.")
        return

    backups.sort(reverse=True)  # Descending order
    latest_backup = os.path.join(backup_dir, backups[0])
    print(f"🔁 Restoring backup: {latest_backup}")

    save_path = get_save_path()
    if not save_path:
        print("❌ Saves folder not found.")
        return

    try:
        with zipfile.ZipFile(latest_backup, 'r') as zip_ref:
            zip_ref.extractall(save_path)
        print("✅ Backup restored successfully.")
    except Exception as e:
        print(f"❌ Error restoring backup: {e}")

def periodic_backup(interval_minutes=10):
    global paused
    while True:
        if not paused:
            create_backup()
        else:
            print("⏸️ Automatic backup paused...")
        time.sleep(interval_minutes * 60)

# Pause/resume functions
def pause_script():
    global paused
    paused = True
    print("⏸️ Script paused (automatic backups stopped).")

def resume_script():
    global paused
    paused = False
    print("▶️ Script resumed (automatic backups active).")

# Launch automatic backup in the background
threading.Thread(target=periodic_backup, args=(10,), daemon=True).start()

# Global shortcuts
keyboard.add_hotkey('f5', create_backup)
keyboard.add_hotkey('f6', load_last_backup)
keyboard.add_hotkey('f7', pause_script)
keyboard.add_hotkey('f8', resume_script)

print("🟢 Automatic backup is active.")
print("🎯 F5: Manual backup | F6: Load latest backup")
print("⏸️ F7: Pause automatic backups | ▶️ F8: Resume automatic backups")

# Keep the script running
keyboard.wait()
