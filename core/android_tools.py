import subprocess
from ppadb.client import Client as AdbClient

class AndroidRepairEngine:
    def __init__(self, host="127.0.0.1", port=5037):
        self.host = host
        self.port = port
        self.client = AdbClient(host=self.host, port=self.port)

    def get_devices(self):
        """Returns a list of connected Android devices."""
        try:
            return self.client.devices()
        except Exception as e:
            print(f"ADB Connection Error: {e}")
            return []

    def clear_all_cache(self, device):
        """Clears cache for all third-party apps."""
        try:
            packages = device.shell("pm list packages -3").splitlines()
            for pkg in packages:
                pkg_name = pkg.replace("package:", "").strip()
                device.shell(f"pm clear {pkg_name}")
            return True
        except Exception:
            return False

    def get_system_info(self, device):
        """Gathers basic device metadata."""
        model = device.shell("getprop ro.product.model").strip()
        version = device.shell("getprop ro.build.version.release").strip()
        return {"model": model, "android_version": version}