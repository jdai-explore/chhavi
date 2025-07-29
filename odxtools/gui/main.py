import sys
import odxtools

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QTextEdit,
)

from .database_explorer import DatabaseExplorer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ODX Tools")

        self.create_actions()
        self.create_menus()
        self.create_toolbars()
        self.create_statusbar()
        self.create_widgets()

    def create_actions(self):
        self.open_action = QAction("&Open...", self)
        self.open_action.triggered.connect(self.open_file)

    def create_menus(self):
        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addAction(self.open_action)
        self.help_menu = self.menuBar().addMenu("&Help")

    def create_toolbars(self):
        self.file_toolbar = self.addToolBar("File")

    def create_statusbar(self):
        self.statusBar().showMessage("Ready")

    def create_widgets(self):
        self.database_explorer = DatabaseExplorer()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.database_explorer)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDX File",
            "",
            "PDX Files (*.pdx)",
        )

        if file_name:
            db = odxtools.load_pdx_file(file_name)
            self.populate_database_explorer(db)

    def populate_database_explorer(self, db):
        model = QStandardItemModel()
        self.database_explorer.tree_view.setModel(model)

        for ecu in db.ecus:
            ecu_item = QStandardItem(ecu.short_name)
            model.appendRow(ecu_item)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
