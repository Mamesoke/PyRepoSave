import os
import zipfile
import shutil
import time
from datetime import datetime
import threading
import keyboard


def get_save_path():
    base = os.getenv("APPDATA")  # Esto da Roaming
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
        print("❌ No se encontró carpeta de saves.")
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

        print(f"✅ Backup creado: {zip_name}")
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")
        return

    # Clean old backups (only we keep last 40 saves)
    try:
        backups = [f for f in os.listdir(backup_dir) if f.endswith(".zip")]
        if len(backups) > 40:
            # Sort by creation date (from oldest to newest)
            backups_full_path = [os.path.join(backup_dir, f) for f in backups]
            backups_full_path.sort(key=os.path.getctime)

            # Delete all except the last 40
            for old_backup in backups_full_path[:-40]:
                os.remove(old_backup)
                print(f"🗑️ Backup eliminado: {old_backup}")
    except Exception as e:
        print(f"⚠️ Error al limpiar backups antiguos: {e}")


def load_last_backup():
    backup_dir = os.path.join(os.getcwd(), "Backups")
    if not os.path.exists(backup_dir):
        print("❌ No existe carpeta de Backups.")
        return

    # Find the latest ZIP file by date
    backups = [f for f in os.listdir(backup_dir) if f.endswith(".zip")]
    if not backups:
        print("❌ No hay backups disponibles.")
        return

    backups.sort(reverse=True)  # Descending order
    latest_backup = os.path.join(backup_dir, backups[0])
    print(f"🔁 Restaurando backup: {latest_backup}")

    save_path = get_save_path()
    if not save_path:
        print("❌ No se encontró carpeta de saves.")
        return

    # Extract ZIP into the saves folder
    try:
        with zipfile.ZipFile(latest_backup, 'r') as zip_ref:
            zip_ref.extractall(save_path)
        print("✅ Backup restaurado con éxito.")
    except Exception as e:
        print(f"❌ Error al restaurar backup: {e}")


def periodic_backup(interval_minutes=10):
    while True:
        create_backup()
        time.sleep(interval_minutes * 60)


# Launch automatic backup in the background
threading.Thread(target=periodic_backup, args=(10,), daemon=True).start()

# Global shortcut to manually save a backup
keyboard.add_hotkey('f5', create_backup)

# Global shortcut to manually load a backup
keyboard.add_hotkey('f6', load_last_backup)

print("🟢 Backup automático activo. Pulsa F5 para guardar backup manual o F6 para cargar el último backup.")
keyboard.wait()  # Keeps the script running
