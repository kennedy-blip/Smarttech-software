import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer

# Path handling for PyInstaller
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
        
        # Core Modules
        self.engine = AndroidRepairEngine()
        self.scanner = MalwareScanner()
        self.ops = AdvancedOperations()
        self.history = RepairHistory()
        self.diag = HardwareDiagnostics()
        self.backup_mgr = BackupManager()
        self.pkg_mgr = PackageManager()
        
        self.actions_performed = []
        self.current_device = None

        # Connect GUI signals to Logic functions
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

    def run_diagnostics(self):
        if not self.current_device: return
        self.window.log("Running hardware diagnostic...")
        data = self.diag.get_battery_report(self.current_device)
        self.window.update_diag_ui(data) # This calls the newly added GUI function

    def run_malware_scan(self):
        if not self.current_device: return
        self.window.log("Scanning for threats...")
        results = self.scanner.scan_device(self.current_device)
        self.window.log(f"Scan Finished. Malicious apps found: {len(results['malware'])}")
        self.actions_performed.append("Security Malware Scan")

    def run_cleaner(self):
        if not self.current_device: return
        self.window.log("Cleaning junk files and cache...")
        if self.engine.clear_all_cache(self.current_device):
            self.window.log("Optimization complete.")
            self.actions_performed.append("System Optimization")

    def run_backup(self):
        if not self.current_device: return
        self.window.log("Backing up DCIM and Documents...")
        msg, _ = self.backup_mgr.backup_device(self.current_device.serial)
        self.window.log(msg)
        self.actions_performed.append("Full Media Backup")

    def run_frp_bypass(self):
        if not self.current_device: return
        self.window.log("Attempting FRP bypass sequence...")
        msg = FRPUnlocker.bypass_setup_wizard(self.current_device)
        self.window.log(msg)
        self.actions_performed.append("FRP Account Bypass")

    def run_factory_reset(self):
        if not self.current_device: return
        confirm = QMessageBox.warning(self.window, "Confirm Wipe", "This will erase ALL data. Continue?", 
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            msg = self.ops.force_factory_reset(self.current_device)
            self.window.log(msg)
            self.actions_performed.append("Full Factory Reset")

    def run_package_manager(self):
        if not self.current_device: return
        pkgs = self.pkg_mgr.get_installed_packages(self.current_device)
        dialog = PackageDialog(pkgs, self.window)
        if dialog.exec():
            selected = dialog.get_selected_packages()
            for p in selected:
                self.pkg_mgr.uninstall_package(self.current_device, p)
            self.window.log(f"Successfully uninstalled {len(selected)} packages.")
            self.actions_performed.append(f"Bloatware Removal ({len(selected)} apps)")

    def generate_report(self):
        if not self.current_device: return
        path = self.history.generate_pdf_report(self.current_device.serial, self.actions_performed)
        self.window.log(f"Invoice generated at: {path}")

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    SmartTechApp().run()
    