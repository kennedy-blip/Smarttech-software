import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer

# --- EXE PATH FIXER ---
# This ensures the EXE can find the 'core' and 'gui' folders inside the temp directory
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
    sys.path.append(bundle_dir)

# Now perform imports
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
        
        # Initialize Core Engines
        self.engine = AndroidRepairEngine()
        self.scanner = MalwareScanner()
        self.ops = AdvancedOperations()
        self.history = RepairHistory()
        self.diag = HardwareDiagnostics()
        self.backup_mgr = BackupManager()
        self.pkg_mgr = PackageManager()
        
        self.actions_performed = []
        self.current_device = None

        # --- Signal Connections ---
        self.window.request_scan.connect(self.run_malware_scan)
        self.window.request_clean.connect(self.run_cleaner)
        self.window.request_reset.connect(self.run_factory_reset)
        self.window.request_diag.connect(self.run_diagnostics)
        self.window.request_report.connect(self.generate_customer_report)
        self.window.request_frp.connect(self.run_frp_bypass)
        self.window.request_backup.connect(self.run_backup)
        self.window.request_packages.connect(self.run_package_manager)

        # Connection Check Timer (Every 3 seconds)
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_connection)
        self.timer.start(3000) 
        self.check_connection()

    def check_connection(self):
        devices = self.engine.get_devices()
        if devices:
            if not self.current_device or self.current_device.serial != devices[0].serial:
                self.current_device = devices[0]
                self.window.status_label.setText(f"ONLINE: {self.current_device.serial}")
                self.window.status_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #a6e3a1;")
                self.window.log(f"Device Ready: {self.current_device.serial}")
                self.run_diagnostics()
        else:
            self.current_device = None
            self.window.status_label.setText("DISCONNECTED")
            self.window.status_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #f38ba8;")

    def run_diagnostics(self):
        if not self.current_device: return
        data = self.diag.get_battery_report(self.current_device)
        self.window.update_diag_ui(data)

    def run_malware_scan(self):
        if not self.current_device: return
        self.window.log("Scanning for malicious packages...")
        results = self.scanner.scan_device(self.current_device)
        self.window.log(f"Found {len(results['malware'])} threats.")
        self.actions_performed.append("Security Scan")

    def run_cleaner(self):
        if not self.current_device: return
        if self.engine.clear_all_cache(self.current_device):
            self.window.log("System cache optimized.")
            self.actions_performed.append("System Deep Clean")

    def run_backup(self):
        if not self.current_device: return
        self.window.log("Starting Backup...")
        msg, details = self.backup_mgr.backup_device(self.current_device.serial)
        self.window.log(msg)
        self.actions_performed.append("Full Data Backup")

    def run_frp_bypass(self):
        if not self.current_device: return
        msg = FRPUnlocker.bypass_setup_wizard(self.current_device)
        self.window.log(msg)
        self.actions_performed.append("FRP Account Unlock")

    def run_factory_reset(self):
        if not self.current_device: return
        msg = self.ops.force_factory_reset(self.current_device)
        self.window.log(msg)
        self.actions_performed.append("Factory Reset")

    def run_package_manager(self):
        if not self.current_device: return
        pkgs = self.pkg_mgr.get_installed_packages(self.current_device)
        dialog = PackageDialog(pkgs, self.window)
        if dialog.exec():
            selected = dialog.get_selected_packages()
            for p in selected:
                self.pkg_mgr.uninstall_package(self.current_device, p)
            self.window.log(f"Removed {len(selected)} apps.")
            self.actions_performed.append(f"Bloatware Removal: {len(selected)} apps")

    def generate_customer_report(self):
        if not self.current_device: return
        path = self.history.generate_pdf_report(self.current_device.serial, self.actions_performed)
        self.window.log(f"Invoice saved to: {path}")

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app_instance = SmartTechApp()
    app_instance.run()