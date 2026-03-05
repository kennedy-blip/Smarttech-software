from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel

class PackageDialog(QDialog):
    def __init__(self, packages, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Bloatware to Remove")
        self.setMinimumSize(400, 600)
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel("Select apps to uninstall (Multi-select enabled):"))
        
        self.list_widget = QListWidget()
        for pkg in packages:
            item = QListWidgetItem(pkg)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(item)
        
        self.layout.addWidget(self.list_widget)

        self.btn_confirm = QPushButton("Uninstall Selected Apps")
        self.btn_confirm.setStyleSheet("background-color: #f38ba8; color: #11111b;")
        self.layout.addWidget(self.btn_confirm)
        
        self.btn_confirm.clicked.connect(self.accept)

    def get_selected_packages(self):
        selected = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected.append(item.text())
        return selected