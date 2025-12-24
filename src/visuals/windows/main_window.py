from __future__ import annotations

import logging
logger = logging.getLogger(__name__)

from PySide6.QtWidgets import QMainWindow
from src.visuals.ui.generated.ui_mainwindow import Ui_MainWindow
from src.visuals.windows.settings import SettingsDialog
from src.visuals.windows.maria_dialog import MariaDialog

from src.utils import writeSettingsFile, readSettingsFile

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionSettings_2.triggered.connect(self.open_settings)
        self.ui.actionMariaDB.triggered.connect(self.open_mariadb_config)
        

    def open_settings(self) -> None:
        dlg = SettingsDialog(self)
        if dlg.exec():  # True wenn accepted
            settings = dlg.get_settings()
            writeSettingsFile(settings, "config/lsas.conf")
            logger.info("general settings saved")

    def open_mariadb_config(self) -> None:
        mdlg = MariaDialog(self)
        if mdlg.exec():
            settings = mdlg.get_settings()
            writeSettingsFile(settings, "config/database.conf")
            logger.info("mariadb settings saved")
