import re

class HardwareDiagnostics:
    def __init__(self):
        self.history = [] # Stores last 20 readings for the graph

    def get_battery_report(self, device):
        try:
            raw_data = device.shell("dumpsys battery")
            level = re.search(r'level:\s+(\d+)', raw_data)
            health = re.search(r'health:\s+(\d+)', raw_data)
            temp = re.search(r'temperature:\s+(\d+)', raw_data)
            
            level_val = int(level.group(1)) if level else 0
            # Keep history for graph (max 20 points)
            self.history.append(level_val)
            if len(self.history) > 20: self.history.pop(0)

            health_map = {2: "Good", 3: "Overheat", 4: "Dead", 5: "Over Volt"}
            
            return {
                "level": level_val,
                "health": health_map.get(int(health.group(1)), "Unknown") if health else "Unknown",
                "temp": int(temp.group(1)) / 10 if temp else 0,
                "history": self.history
            }
        except:
            return None