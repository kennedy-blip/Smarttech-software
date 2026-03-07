import os

class AdvancedOperations:
    @staticmethod
    def force_factory_reset(device):
        """Factory Reset: Triggers the recovery wipe sequence."""
        try:
            # Standard recovery wipe command
            device.shell("recovery --wipe_data")
            # Alternative: Broadcasting the Master Clear intent
            device.shell("am broadcast -a android.intent.action.MASTER_CLEAR")
            return "Factory Reset command sent. The device should reboot into recovery."
        except Exception as e:
            return f"Wipe Error: {str(e)}"

    @staticmethod
    def set_lock_screen_note(device, message):
        """Lock Note: Injects a custom string into the lock screen owner info."""
        try:
            # Write to the 'Secure' settings table
            device.shell(f"settings put secure lock_screen_owner_info '{message}'")
            # Toggle the visibility bit to '1' (enabled)
            device.shell("settings put secure lock_screen_owner_info_enabled 1")
            return f"Lock screen updated successfully: {message}"
        except Exception as e:
            return f"Failed to set Lock Note: {str(e)}"

class FRPUnlocker:
    @staticmethod
    def bypass_setup_wizard(device):
        """FRP Bypass: Disables the setup wizard app and flags the device as provisioned."""
        try:
            # Method 1: Force disable the Setup Wizard package
            device.shell("pm disable com.google.android.setupwizard")
            
            # Method 2: Manually flag the device as 'Setup Complete' in settings
            device.shell("settings put global setup_wizard_has_run 1")
            device.shell("settings put secure user_setup_complete 1")
            device.shell("settings put global device_provisioned 1")
            
            return "FRP Bypass commands sent. Check if the device proceeds to Home Screen."
        except Exception as e:
            return f"Bypass Error: {str(e)}"