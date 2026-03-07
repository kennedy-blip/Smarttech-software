import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer

from gui.main_window import SmartTechGUI
from gui.package_view import PackageDialog
from core.android_tools import AndroidRepairEngine
from core.advanced_ops import AdvancedOperations, FRPUnlocker
from core.diagnostics import HardwareDiagnostics
from core.package_manager import PackageManager
from core.backup_manager import BackupManager

class SmartTechApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = SmartTechGUI()
        
        # Engines
        self.engine = AndroidRepairEngine()
        self.ops = AdvancedOperations()
        self.diag = HardwareDiagnostics()
        self.pkg_mgr = PackageManager()
        self.backup_mgr = BackupManager()
        
        self.current_device = None

        # Link GUI to Functions
        self.window.request_packages.connect(self.run_pkgs)
        self.window.request_diag.connect(self.run_diag)
        self.window.request_backup.connect(self.run_backup)
        self.window.request_clean.connect(self.run_clean)
        self.window.request_frp.connect(self.run_frp)
        self.window.request_reset.connect(self.run_reset)
        self.window.request_note.connect(self.run_note)
        self.window.request_push.connect(self.run_push)

        # Polling Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_conn)
        self.timer.start(2000)

    def check_conn(self):
        devs = self.engine.get_devices()
        if devs:
            if not self.current_device or self.current_device.serial != devs[0].serial:
                self.current_device = devs[0]
                info = self.engine.get_device_info(self.current_device)
                self.window.lbl_model.setText(f"Model: {info['model']} (V{info['version']})")
                self.window.lbl_status.setText("ONLINE")
                self.window.lbl_status.setStyleSheet("color: #a6e3a1; font-weight: bold;")
                self.window.log(f"Connected: {info['model']}")
        else:
            if self.current_device:
                self.current_device = None
                self.window.lbl_model.setText("Model: Waiting for Device...")
                self.window.lbl_status.setText("OFFLINE")
                self.window.lbl_status.setStyleSheet("color: #f38ba8; font-weight: bold;")

    def run_diag(self):
        if self.current_device:
            d = self.diag.get_battery_report(self.current_device)
            if d: self.window.update_battery_ui(d['level'], d['health'], d['temp'])

    def run_pkgs(self):
        if self.current_device:
            pkgs = self.pkg_mgr.get_installed_packages(self.current_device)
            dialog = PackageDialog(pkgs, self.window)
            if dialog.exec():
                for p in dialog.get_selected_packages():
                    self.pkg_mgr.uninstall_package(self.current_device, p)
                    self.window.log(f"Removed: {p}")

    def run_frp(self):
        if self.current_device: self.window.log(FRPUnlocker.bypass_setup_wizard(self.current_device))

    def run_reset(self):
        if self.current_device:
            if QMessageBox.warning(self.window, "Confirm", "Wipe all data?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
                self.window.log(self.ops.force_factory_reset(self.current_device))

    def run_note(self, text):
        if self.current_device: self.window.log(self.ops.set_lock_screen_note(self.current_device, text))

    def run_push(self, path):
        if self.current_device:
            s, res = self.engine.push_file(self.current_device, path)
            self.window.log(f"File Push {'Success' if s else 'Failed'}: {res}")

    def run_backup(self):
        if self.current_device:
            msg, _ = self.backup_mgr.backup_device(self.current_device.serial)
            self.window.log(msg)

    def run_clean(self):
        if self.current_device:
            self.engine.clear_all_cache(self.current_device)
            self.window.log("Cache Cleaned.")

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    SmartTechApp().run()