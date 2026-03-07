from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QProgressBar, QHBoxLayout, QFrame, QTextEdit,
                             QInputDialog, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal

class SmartTechGUI(QMainWindow):
    # Communication Signals
    request_scan = pyqtSignal()
    request_clean = pyqtSignal()
    request_reset = pyqtSignal()
    request_diag = pyqtSignal()
    request_frp = pyqtSignal()
    request_backup = pyqtSignal()
    request_packages = pyqtSignal()
    request_note = pyqtSignal(str)
    request_push = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartTech Ultimate Suite 2026")
        self.setMinimumSize(1100, 750)
        
        # Modern Dark Theme
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QLabel { color: #cdd6f4; font-family: 'Segoe UI'; }
            QFrame#card { background-color: #313244; border-radius: 12px; }
            QPushButton { 
                background-color: #45475a; color: white; border-radius: 8px; 
                padding: 12px; font-weight: bold; 
            }
            QPushButton:hover { background-color: #585b70; border: 1px solid #89b4fa; }
            QPushButton#danger { background-color: #f38ba8; color: #11111b; }
            QTextEdit { background-color: #11111b; color: #a6e3a1; font-family: 'Consolas'; padding: 10px; }
            QProgressBar {
                border: 2px solid #313244; border-radius: 5px; text-align: center;
                background-color: #181825; color: white;
            }
            QProgressBar::chunk { background-color: #a6e3a1; }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_main = QHBoxLayout(self.central_widget)

        # --- SIDEBAR ---
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        
        self.btn_pkg = QPushButton("📦 Manage Apps")
        self.btn_diag = QPushButton("🔋 Battery Health")
        self.btn_backup = QPushButton("💾 Full Backup")
        self.btn_clean = QPushButton("🧹 Deep Clean")
        
        for btn in [self.btn_pkg, self.btn_diag, self.btn_backup, self.btn_clean]:
            self.sidebar_layout.addWidget(btn)
        self.sidebar_layout.addStretch()
        self.layout_main.addWidget(self.sidebar)

        # --- CONTENT AREA ---
        self.content_layout = QVBoxLayout()

        # Device Info Card
        self.info_card = QFrame()
        self.info_card.setObjectName("card")
        self.info_box = QHBoxLayout(self.info_card)
        self.lbl_model = QLabel("Model: Waiting for Device...")
        self.lbl_status = QLabel("OFFLINE")
        self.lbl_status.setStyleSheet("color: #f38ba8; font-weight: bold; font-size: 16px;")
        self.info_box.addWidget(self.lbl_model)
        self.info_box.addStretch()
        self.info_box.addWidget(self.lbl_status)
        self.content_layout.addWidget(self.info_card)

        # Battery Visualizer
        self.batt_card = QFrame()
        self.batt_card.setObjectName("card")
        self.batt_box = QVBoxLayout(self.batt_card)
        self.lbl_batt_text = QLabel("Battery Level: -- %")
        self.batt_bar = QProgressBar()
        self.batt_box.addWidget(self.lbl_batt_text)
        self.batt_box.addWidget(self.batt_bar)
        self.content_layout.addWidget(self.batt_card)

        # Console
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.content_layout.addWidget(self.terminal)

        # Tools Row
        self.tool_row = QHBoxLayout()
        self.btn_note = QPushButton("🔑 Set Lock Note")
        self.btn_push = QPushButton("📂 Push File")
        self.tool_row.addWidget(self.btn_note)
        self.tool_row.addWidget(self.btn_push)
        self.content_layout.addLayout(self.tool_row)

        # Danger Zone
        self.danger_row = QHBoxLayout()
        self.btn_frp = QPushButton("🔓 FRP BYPASS")
        self.btn_reset = QPushButton("⚠️ FACTORY RESET")
        self.btn_frp.setObjectName("danger")
        self.btn_reset.setObjectName("danger")
        self.danger_row.addWidget(self.btn_frp)
        self.danger_row.addWidget(self.btn_reset)
        self.content_layout.addLayout(self.danger_row)

        self.layout_main.addLayout(self.content_layout)

        # Signal Triggers
        self.btn_pkg.clicked.connect(self.request_packages.emit)
        self.btn_diag.clicked.connect(self.request_diag.emit)
        self.btn_backup.clicked.connect(self.request_backup.emit)
        self.btn_clean.clicked.connect(self.request_clean.emit)
        self.btn_frp.clicked.connect(self.request_frp.emit)
        self.btn_reset.clicked.connect(self.request_reset.emit)
        self.btn_note.clicked.connect(self.get_note_input)
        self.btn_push.clicked.connect(self.get_file_input)

    def log(self, message):
        self.terminal.append(f"<span style='color: #89b4fa;'>[SYSTEM]</span> {message}")

    def update_battery_ui(self, level, health, temp):
        self.batt_bar.setValue(level)
        self.lbl_batt_text.setText(f"Battery: {level}% | Health: {health} | Temp: {temp}°C")

    def get_note_input(self):
        text, ok = QInputDialog.getText(self, "Lock Note", "Enter Shop Name/Note:")
        if ok and text: self.request_note.emit(text)

    def get_file_input(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File to Push")
        if path: self.request_push.emit(path)