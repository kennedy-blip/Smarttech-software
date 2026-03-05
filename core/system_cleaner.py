class SystemCleaner:
    @staticmethod
    def deep_clean(device):
        """Clears cache for every user-installed app."""
        packages = device.shell("pm list packages -3").splitlines()
        for pkg in packages:
            name = pkg.replace("package:", "").strip()
            # This is the equivalent of 'Clear Cache' in settings
            device.shell(f"pm trim-caches 999G") 
            device.shell(f"rm -rf /sdcard/Android/data/{name}/cache/*")
        return True