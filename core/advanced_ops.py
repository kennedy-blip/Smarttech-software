import time

class AdvancedOperations:
    @staticmethod
    def force_factory_reset(device):
        """Sends the reboot command to enter recovery mode for a wipe."""
        try:
            device.shell("reboot recovery")
            return "SUCCESS: Device rebooting to Recovery. Manually select 'Wipe Data' if prompted."
        except Exception as e:
            return f"ERROR: Could not initiate reset: {e}"

    @staticmethod
    def trigger_system_update(device):
        """Attempts to force the Google Services Framework to check for updates."""
        try:
            # Clears the GSF cache to force a fresh check-in with Google servers
            device.shell("pm clear com.google.android.gsf")
            device.shell("am start -n com.google.android.gms/.update.SystemUpdateActivity")
            return "SUCCESS: System update check forced. See phone screen."
        except Exception as e:
            return f"ERROR: Update trigger failed: {e}"