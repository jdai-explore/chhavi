import sys
import odxtools
from odxtools.diaglayers.diaglayer import DiagLayer
from odxtools.diagservice import DiagService as Service
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
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
        # Database Explorer is already a QDockWidget
        self.database_explorer = DatabaseExplorer()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.database_explorer)

        # Create and add Service Editor dock widget
        self.service_editor = ServiceEditor()
        service_dock = QDockWidget("Service Editor", self)
        service_dock.setWidget(self.service_editor)
        self.addDockWidget(Qt.RightDockWidgetArea, service_dock)

        # Create and add DTC Viewer dock widget
        self.dtc_viewer = DTCViewer()
        dtc_dock = QDockWidget("DTC Viewer", self)
        dtc_dock.setWidget(self.dtc_viewer)
        self.addDockWidget(Qt.BottomDockWidgetArea, dtc_dock)

        # Create and add Communication Console dock widget
        self.communication_console = CommunicationConsole()
        console_dock = QDockWidget("Communication Console", self)
        console_dock.setWidget(self.communication_console)
        self.addDockWidget(Qt.BottomDockWidgetArea, console_dock)
        
        # Tabify the bottom dock widgets
        self.tabifyDockWidget(dtc_dock, console_dock)

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

        if isinstance(item_data, DiagLayer):
            self.dtc_viewer.set_ecu(item_data)
        elif isinstance(item_data, Service):
            self.service_editor.set_service(item_data)

    def populate_database_explorer(self, db):
        model = QStandardItemModel()
        self.database_explorer.tree_view.setModel(model)
        self.database_explorer.tree_view.selectionModel().selectionChanged.connect(self.item_selected)

        for ecu in db.ecus:
            ecu_item = QStandardItem(ecu.short_name)
            ecu_item.setData(ecu, Qt.UserRole)
            model.appendRow(ecu_item)

            diag_layer = ecu.diag_layer_raw
            if hasattr(diag_layer, 'services'):
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
