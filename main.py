import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer

# Path handling for PyInstaller bundling
if getattr(sys, 'frozen', False):
    sys.path.append(sys._MEIPASS)

from gui.main_window import SmartTechGUI
from gui.package_view import PackageDialog
from core.android_tools import AndroidRepairEngine
from core.malware_scan import MalwareScanner
from core.advanced_ops import AdvancedOperations
from core.history_manager import RepairHistory
from core.diagnostics import HardwareDiagnostics
from core.frp_tools import FRPUnlocker
from core.backup_manager import BackupManager
from core.package_manager import PackageManager

class SmartTechApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = SmartTechGUI()
        
        # Core Logic Modules
        self.engine = AndroidRepairEngine()
        self.scanner = MalwareScanner()
        self.ops = AdvancedOperations()
        self.history = RepairHistory()
        self.diag = HardwareDiagnostics()
        self.backup_mgr = BackupManager()
        self.pkg_mgr = PackageManager()
        
        self.actions_performed = []
        self.current_device = None

        # Signals
        self.window.request_scan.connect(self.run_malware_scan)
        self.window.request_clean.connect(self.run_cleaner)
        self.window.request_backup.connect(self.run_backup)
        self.window.request_frp.connect(self.run_frp_bypass)
        self.window.request_reset.connect(self.run_factory_reset)
        self.window.request_diag.connect(self.run_diagnostics)
        self.window.request_packages.connect(self.run_package_manager)
        self.window.request_report.connect(self.generate_report)

        # Connection polling
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_connection)
        self.timer.start(3000)

    def check_connection(self):
        devices = self.engine.get_devices()
        if devices:
            if not self.current_device or self.current_device.serial != devices[0].serial:
                self.current_device = devices[0]
                self.window.status_label.setText(f"ONLINE: {self.current_device.serial}")
                self.window.status_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #a6e3a1;")
                self.window.log(f"Device connected: {self.current_device.serial}")
        else:
            self.current_device = None
            self.window.status_label.setText("DISCONNECTED")
            self.window.status_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #f38ba8;")

    def run_package_manager(self):
        """Safe execution of the App Manager to prevent software crashes."""
        if not self.current_device:
            self.window.log("Error: Connect a device first.")
            return
        
        try:
            self.window.log("Fetching package list...")
            # Get list from package manager
            pkgs = self.pkg_mgr.get_installed_packages(self.current_device)
            
            # Show Dialog
            dialog = PackageDialog(pkgs, self.window)
            if dialog.exec():
                selected = dialog.get_selected_packages()
                if not selected:
                    self.window.log("No apps selected.")
                    return
                
                self.window.log(f"Starting removal of {len(selected)} apps...")
                for p in selected:
                    if self.pkg_mgr.uninstall_package(self.current_device, p):
                        self.window.log(f"Successfully uninstalled: {p}")
                    else:
                        self.window.log(f"Failed to remove: {p}")
                
                self.actions_performed.append(f"Bloatware Removal: {len(selected)} apps")
        
        except Exception as e:
            # This captures any error and prevents the app from closing
            self.window.log(f"CRITICAL ERROR in App Manager: {str(e)}")
            print(f"Debug Info: {e}")

    # --- Other Methods ---
    def run_diagnostics(self):
        if self.current_device:
            self.window.log("Gathering hardware metrics...")
            data = self.diag.get_battery_report(self.current_device)
            self.window.update_diag_ui(data)

    def run_malware_scan(self):
        if self.current_device:
            self.window.log("Scanning system...")
            results = self.scanner.scan_device(self.current_device)
            self.window.log(f"Scan complete. {len(results['malware'])} threats.")
            self.actions_performed.append("Security Scan")

    def run_cleaner(self):
        if self.current_device:
            if self.engine.clear_all_cache(self.current_device):
                self.window.log("Deep Clean Finished.")
                self.actions_performed.append("System Optimization")

    def run_backup(self):
        if self.current_device:
            msg, _ = self.backup_mgr.backup_device(self.current_device.serial)
            self.window.log(msg)
            self.actions_performed.append("Data Backup")

    def run_frp_bypass(self):
        if self.current_device:
            msg = FRPUnlocker.bypass_setup_wizard(self.current_device)
            self.window.log(msg)
            self.actions_performed.append("FRP Bypass")

    def run_factory_reset(self):
        if self.current_device:
            msg = self.ops.force_factory_reset(self.current_device)
            self.window.log(msg)
            self.actions_performed.append("Factory Reset")

    def generate_report(self):
        if self.current_device:
            path = self.history.generate_pdf_report(self.current_device.serial, self.actions_performed)
            self.window.log(f"Report saved: {path}")

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    SmartTechApp().run()