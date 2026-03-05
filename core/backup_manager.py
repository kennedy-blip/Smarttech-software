import os
import subprocess

class BackupManager:
    def __init__(self, base_backup_dir="C:/SmartTech_Backups"):
        self.base_dir = base_backup_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def backup_device(self, device_serial):
        """Pulls DCIM (Photos) and Documents from the device."""
        customer_dir = os.path.join(self.base_dir, device_serial)
        if not os.path.exists(customer_dir):
            os.makedirs(customer_dir)

        # We use the raw ADB command for 'pull' because it's faster for large files
        paths_to_backup = [
            "/sdcard/DCIM",
            "/sdcard/Pictures",
            "/sdcard/Download",
            "/sdcard/Documents"
        ]
        
        results = []
        for path in paths_to_backup:
            # Command: adb -s [serial] pull [remote_path] [local_destination]
            cmd = f"adb -s {device_serial} pull {path} {customer_dir}"
            try:
                subprocess.run(cmd, shell=True, check=True, capture_output=True)
                results.append(f"Successfully backed up: {path}")
            except subprocess.CalledProcessError:
                results.append(f"Failed or Empty: {path}")
        
        return f"Backup complete. Files stored in: {customer_dir}", results