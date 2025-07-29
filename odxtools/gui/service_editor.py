from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ServiceEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Select a service to view details.")
        layout.addWidget(self.label)

    def set_service(self, service):
        self.label.setText(f"Service: {service.short_name}")
