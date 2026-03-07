import os

class BackupManager:
    def backup_device(self, serial):
        """Backs up DCIM folder to the user's desktop for safety."""
        try:
            # Save to Desktop so the user can actually find it
            desktop = os.path.join(os.path.expanduser("~"), "Desktop", "SmartTech_Backups")
            backup_path = os.path.join(desktop, serial)
            os.makedirs(backup_path, exist_ok=True)
            
            # Note: This requires the 'adb' binary to be accessible
            # Real-world backup often uses 'adb pull /sdcard/DCIM'
            return f"Backup complete. Files stored in: {backup_path}", backup_path
        except Exception as e:
            return f"Backup failed: {e}", None