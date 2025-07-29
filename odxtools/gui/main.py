import sys
import odxtools
import odxtools.ecu
import odxtools.service

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QTextEdit,
)

from .database_explorer import DatabaseExplorer
from .service_editor import ServiceEditor
from .dtc_viewer import DTCViewer
from .communication_console import CommunicationConsole


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
        self.database_explorer.tree_view.selectionModel().selectionChanged.connect(self.item_selected)

        self.service_editor = ServiceEditor()
        self.addDockWidget(Qt.RightDockWidgetArea, self.service_editor)

        self.dtc_viewer = DTCViewer()
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dtc_viewer)

        self.communication_console = CommunicationConsole()
        self.tabifyDockWidget(self.dtc_viewer, self.communication_console)

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

    def item_selected(self, selected, deselected):
        if not selected.indexes():
            return

        index = selected.indexes()[0]
        item_data = index.data(Qt.UserRole)

        if isinstance(item_data, odxtools.ecu.Ecu):
            self.dtc_viewer.set_ecu(item_data)
        elif isinstance(item_data, odxtools.service.Service):
            self.service_editor.set_service(item_data)

    def populate_database_explorer(self, db):
        model = QStandardItemModel()
        self.database_explorer.tree_view.setModel(model)

        for ecu in db.ecus:
            ecu_item = QStandardItem(ecu.short_name)
            ecu_item.setData(ecu, Qt.UserRole)
            model.appendRow(ecu_item)

            diag_layer = ecu.diag_layer
            for service in diag_layer.services:
                service_item = QStandardItem(service.short_name)
                service_item.setData(service, Qt.UserRole)
                ecu_item.appendRow(service_item)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
