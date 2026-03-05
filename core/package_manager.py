class PackageManager:
    @staticmethod
    def get_installed_packages(device, user_only=True):
        """
        Returns a list of packages. 
        user_only=True shows only apps installed by the user/manufacturer.
        """
        cmd = "pm list packages -3" if user_only else "pm list packages"
        raw_list = device.shell(cmd).splitlines()
        packages = [pkg.replace("package:", "").strip() for pkg in raw_list]
        return sorted(packages)

    @staticmethod
    def uninstall_package(device, package_name):
        """Removes a specific app from the device."""
        try:
            # -k keeps data, but since we are 'cleaning', we do a full removal
            result = device.shell(f"pm uninstall {package_name}")
            return "Success" in result
        except Exception as e:
            print(f"Uninstall Error: {e}")
            return False