import re

class HardwareDiagnostics:
    @staticmethod
    def get_battery_report(device):
        """Fetches and parses real-time battery data from the device."""
        try:
            # Get raw dump from the Android system
            raw_data = device.shell("dumpsys battery")
            
            # Use Regex to find values (handles different spacing/formats)
            level = re.search(r'level:\s+(\d+)', raw_data)
            health = re.search(r'health:\s+(\d+)', raw_data)
            temp = re.search(r'temperature:\s+(\d+)', raw_data)
            voltage = re.search(r'voltage:\s+(\d+)', raw_data)

            # Convert Android Health ID to Human Readable Text
            health_map = {
                1: "Unknown",
                2: "Good",
                3: "Overheating",
                4: "Dead",
                5: "Over Voltage",
                6: "Unspecified Failure",
                7: "Cold"
            }

            # Parse temperature (Android returns it in tenths of a degree, e.g., 350 = 35.0°C)
            temp_val = int(temp.group(1)) / 10 if temp else 0
            
            # Parse voltage (Android returns it in millivolts, e.g., 4200 = 4.2V)
            volt_val = int(voltage.group(1)) / 1000 if voltage else 0

            return {
                "level": level.group(1) if level else "0",
                "health": health_map.get(int(health.group(1)), "Unknown") if health else "Unknown",
                "temp": f"{temp_val:.1f}",
                "voltage": f"{volt_val:.2f}"
            }
        except Exception as e:
            print(f"Diag Error: {e}")
            return None