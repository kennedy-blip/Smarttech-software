from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QProgressBar, QHBoxLayout, QFrame, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal

class SmartTechGUI(QMainWindow):
    # Signals for logic communication
    request_scan = pyqtSignal()
    request_clean = pyqtSignal()
    request_reset = pyqtSignal()
    request_diag = pyqtSignal()
    request_report = pyqtSignal()
    request_frp = pyqtSignal()
    request_backup = pyqtSignal()
    request_packages = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartTech Pro Repair Suite | 2026 Edition")
        self.setMinimumSize(1000, 700)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QLabel { color: #cdd6f4; font-family: 'Segoe UI'; }
            QFrame#card { 
                background-color: #313244; border-radius: 10px; border: 1px solid #45475a;
            }
            QPushButton { 
                background-color: #45475a; color: white; border-radius: 6px; 
                padding: 10px; font-weight: bold;
            }
            QPushButton:hover { background-color: #585b70; border: 1px solid #89b4fa; }
            QPushButton#danger_btn { background-color: #f38ba8; color: #11111b; }
            QPushButton#success_btn { background-color: #a6e3a1; color: #11111b; }
            QProgressBar { 
                border-radius: 10px; text-align: center; color: white; background-color: #181825;
            }
            QProgressBar::chunk { background-color: #89b4fa; border-radius: 10px; }
            QTextEdit { background-color: #11111b; color: #a6e3a1; font-family: 'Consolas'; font-size: 12px; }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # --- SIDEBAR ---
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setObjectName("card")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        
        self.sidebar_layout.addWidget(QLabel("🔧 SMARTTECH MENU"))
        self.btn_diag = QPushButton("🔋 Battery Health")
        self.btn_pkg = QPushButton("📦 Manage Apps")
        self.sidebar_layout.addWidget(self.btn_diag)
        self.sidebar_layout.addWidget(self.btn_pkg)
        self.sidebar_layout.addStretch()
        self.main_layout.addWidget(self.sidebar)

        # --- MAIN CONTENT ---
        self.content_layout = QVBoxLayout()

        # Status Display
        self.status_card = QFrame()
        self.status_card.setObjectName("card")
        self.status_vbox = QVBoxLayout(self.status_card)
        self.status_label = QLabel("DISCONNECTED")
        self.status_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #f38ba8;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_vbox.addWidget(self.status_label)
        self.content_layout.addWidget(self.status_card)

        # Progress
        self.progress = QProgressBar()
        self.content_layout.addWidget(self.progress)

        # Basic Actions
        self.actions_layout = QHBoxLayout()
        self.btn_scan = QPushButton("Malware Scan")
        self.btn_clean = QPushButton("Deep Clean")
        self.btn_backup = QPushButton("💾 Backup Media")
        self.btn_backup.setObjectName("success_btn")
        self.actions_layout.addWidget(self.btn_scan)
        self.actions_layout.addWidget(self.btn_clean)
        self.actions_layout.addWidget(self.btn_backup)
        self.content_layout.addLayout(self.actions_layout)

        # Advanced Actions
        self.danger_card = QFrame()
        self.danger_card.setObjectName("card")
        self.danger_card.setStyleSheet("border: 1px solid #f38ba8;")
        self.danger_layout = QHBoxLayout(self.danger_card)
        self.btn_frp = QPushButton("🔓 Bypass FRP Lock")
        self.btn_frp.setObjectName("danger_btn")
        self.btn_reset = QPushButton("⚠️ Factory Reset")
        self.btn_reset.setObjectName("danger_btn")
        self.danger_layout.addWidget(self.btn_frp)
        self.danger_layout.addWidget(self.btn_reset)
        self.content_layout.addWidget(self.danger_card)

        # Console
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.content_layout.addWidget(self.terminal)

        # Footer
        self.btn_report = QPushButton("Generate Official Repair Invoice")
        self.btn_report.setObjectName("success_btn")
        self.content_layout.addWidget(self.btn_report)

        self.main_layout.addLayout(self.content_layout)

        # Signals
        self.btn_scan.clicked.connect(self.request_scan.emit)
        self.btn_clean.clicked.connect(self.request_clean.emit)
        self.btn_backup.clicked.connect(self.request_backup.emit)
        self.btn_frp.clicked.connect(self.request_frp.emit)
        self.btn_reset.clicked.connect(self.request_reset.emit)
        self.btn_diag.clicked.connect(self.request_diag.emit)
        self.btn_pkg.clicked.connect(self.request_packages.emit)
        self.btn_report.clicked.connect(self.request_report.emit)

    def log(self, message):
        self.terminal.append(f"> {message}")

    def update_diag_ui(self, data):
        """Fixed: Now correctly updates the terminal with battery health info."""
        if not data:
            self.log("Diagnostic Error: Could not retrieve battery data.")
            return

        report = (
            f"\n[BATTERY HEALTH REPORT]\n"
            f"● Charge Level: {data.get('level', '??')}% \n"
            f"● Health Status: {data.get('health', 'Unknown')} \n"
            f"● Temperature: {data.get('temp', '??')}°C \n"
            f"● Voltage: {data.get('voltage', '??')}V\n"
        )
        self.log(report)