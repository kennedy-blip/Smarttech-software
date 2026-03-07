import subprocess
import os
import sys
from ppadb.client import Client as AdbClient

class AndroidRepairEngine:
    def __init__(self, host="127.0.0.1", port=5037):
        self.host = host
        self.port = port
        self.adb_path = self._get_adb_path()
        self.ensure_adb_running() 
        self.client = AdbClient(host=self.host, port=self.port)

    def _get_adb_path(self):
        """Locates the adb binary for script or compiled EXE mode."""
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, "bin", "adb.exe")

    def ensure_adb_running(self):
        """Starts the ADB server in the background without a CMD window popping up."""
        try:
            subprocess.run([self.adb_path, "start-server"], 
                           check=True, capture_output=True,
                           creationflags=0x08000000) # CREATE_NO_WINDOW
        except Exception as e:
            print(f"ADB Server Boot Error: {e}")

    def get_devices(self):
        """Retrieves list of active device objects."""
        try:
            return self.client.devices()
        except:
            self.ensure_adb_running()
            return []

    def get_device_info(self, device):
        """Gathers basic identity properties from the Android build prop."""
        try:
            model = device.shell("getprop ro.product.model").strip()
            brand = device.shell("getprop ro.product.brand").strip()
            version = device.shell("getprop ro.build.version.release").strip()
            return {
                "model": f"{brand.upper()} {model}",
                "version": f"Android {version}"
            }
        except:
            return {"model": "Unknown Device", "version": "?"}

    def push_file(self, device, local_path):
        """File Push: Transfers a file to /sdcard/Download/."""
        try:
            file_name = os.path.basename(local_path)
            remote_path = f"/sdcard/Download/{file_name}"
            
            # Using binary stream for reliable transfer
            with open(local_path, 'rb') as f:
                device.push(f, remote_path)
            return True, remote_path
        except Exception as e:
            return False, str(e)

    def clear_all_cache(self, device):
        """Optimization: Clears data for all non-system applications."""
        try:
            packages = device.shell("pm list packages -3").splitlines()
            for pkg in packages:
                pkg_name = pkg.replace("package:", "").strip()
                if pkg_name:
                    device.shell(f"pm clear {pkg_name}")
            return True
        except:
            return False