from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeView


class DatabaseExplorer(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        # Show context menu based on selected item
        pass
