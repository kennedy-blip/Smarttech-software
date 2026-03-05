from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QListWidget, 
                             QListWidgetItem, QPushButton, QLabel)
from PyQt6.QtCore import Qt  # <--- CRITICAL: Required for CheckStates

class PackageDialog(QDialog):
    def __init__(self, packages, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SmartTech Bulk Uninstaller")
        self.setMinimumSize(450, 600)
        self.layout = QVBoxLayout(self)

        # Header
        self.layout.addWidget(QLabel("<b>Select Bloatware to Remove:</b>"))
        self.layout.addWidget(QLabel("<i>Note: Only third-party/user apps are listed here.</i>"))
        
        # App List
        self.list_widget = QListWidget()
        for pkg in packages:
            item = QListWidgetItem(pkg)
            # Correct PyQt6 syntax for checkboxes
            item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(item)
        
        self.layout.addWidget(self.list_widget)

        # Buttons
        self.btn_confirm = QPushButton("Uninstall Selected Packages")
        self.btn_confirm.setStyleSheet("""
            background-color: #f38ba8; 
            color: #11111b; 
            font-weight: bold; 
            padding: 12px;
        """)
        self.layout.addWidget(self.btn_confirm)
        
        # Connect button to "accept" which closes the dialog and returns execution to main
        self.btn_confirm.clicked.connect(self.accept)

    def get_selected_packages(self):
        """Returns a list of strings for every checked item."""
        selected = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected.append(item.text())
        return selected