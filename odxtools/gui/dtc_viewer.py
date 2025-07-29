from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class DTCViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Select an ECU to view DTCs.")
        layout.addWidget(self.label)

    def set_ecu(self, ecu):
        self.label.setText(f"ECU: {ecu.short_name}")
