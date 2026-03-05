class HardwareDiagnostics:
    @staticmethod
    def get_battery_report(device):
        """Pulls deep battery telemetry."""
        raw_data = device.shell("dumpsys battery")
        
        # Parse the raw text into a dictionary
        stats = {}
        for line in raw_data.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                stats[key.strip()] = value.strip()
        
        # Logic to determine health status
        level = stats.get("level", "0")
        health_code = stats.get("health", "1")
        
        # Health codes: 2 = Good, 3 = Overheat, 4 = Dead, 5 = Overvoltage
        health_map = {"2": "Good", "3": "Overheat", "4": "Degraded", "5": "Voltage Issue"}
        health_str = health_map.get(health_code, "Unknown")
        
        return {
            "Level": f"{level}%",
            "Status": health_str,
            "Temp": f"{int(stats.get('temperature', 0)) / 10}°C",
            "Cycles": stats.get("counter", "N/A") # Cycle count on supported kernels
        }