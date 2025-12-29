from __future__ import annotations

import logging
logger = logging.getLogger(__name__)

from PySide6.QtWidgets import QMainWindow, QFileDialog, QCheckBox
from src.visuals.ui.generated.ui_mainwindow import Ui_MainWindow
from src.visuals.windows.settings import SettingsDialog
from src.visuals.windows.maria_dialog import MariaDialog

from src.core.ops import importMatchfileData, clearData, databaseSetup

from src.utils import writeSettingsFile, readSettingsFile, getRelPath

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.settings = readSettingsFile(".config/lsas.conf")

        if self.settings["mariadb"] == "0":
            self.ui.radio_db_create.setCheckable(False)

        self.ui.button_execute.clicked.connect(self.execute_radio)
        self.ui.actionSettings_2.triggered.connect(self.open_settings)
        self.ui.actionMariaDB.triggered.connect(self.open_mariadb_config)
        self.ui.actionImport_Matchfile.triggered.connect(self.filedialog_opener)

    def execute_radio(self) -> None:
        if self.ui.radio_clear.isChecked():
            clearData()
        if self.ui.radio_db_create.isChecked():
            databaseSetup() 

    def filedialog_opener(self) -> None:
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Matchfiles (*.json)")
        dialog.setViewMode(QFileDialog.Detail)
        dialog.selectFile("./")
        if dialog.exec_():
            
            fileNames = dialog.selectedFiles()
            for file in fileNames:
                importMatchfileData(str(getRelPath(file)))
        #self.

    def open_settings(self) -> None:
        dlg = SettingsDialog(self)
        if dlg.exec():  # True wenn accepted
            settings = dlg.get_settings()
            if settings["mariadb"] == "1":
                self.ui.radio_db_create.setCheckable(True)
            else:
                self.ui.radio_db_create.setCheckable(False)
            writeSettingsFile(settings, ".config/lsas.conf")
            logger.info("general settings saved")

    def open_mariadb_config(self) -> None:
        mdlg = MariaDialog(self)
        if mdlg.exec():
            settings = mdlg.get_settings()
            writeSettingsFile(settings, ".config/database.conf")
            logger.info("mariadb settings saved")
