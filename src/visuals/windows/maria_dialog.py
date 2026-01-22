from __future__ import annotations

import time

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer
from src.visuals.ui.generated.ui_maria_dialog import Ui_Dialog

from src.core.io.mariadb import updateConnectionState
from src.core.config import config, Configs

class MariaDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.timer = QTimer(self)

        # init settings
        self._init_fields()

        # try a connection
        self.timer.timeout.connect(self._restore_button)
        self.ui.pushButton_connection.clicked.connect(self._try_connection)

    def _init_fields(self) -> None:
        """initializes the current fields with values of mariadb.conf"""
        if config.volatile_settings["_connected"] == "1":
            self.ui.pushButton_connection.setText("connected!")
            self.ui.pushButton_connection.setDisabled(True)

        self.ui.lineEdit_adress.setText(config.general_settings[Configs.DB]["host"])
        self.ui.lineEdit_db.setText(config.general_settings[Configs.DB]["database"])
        self.ui.lineEdit_port.setText(config.general_settings[Configs.DB]["port"])
        self.ui.lineEdit_pw.setText(config.general_settings[Configs.DB]["password"])
        self.ui.lineEdit_un.setText(config.general_settings[Configs.DB]["user"])

    def _try_connection(self) -> None:
        """connection test, which also writes settings according to the outcome"""
        self.saveSettings()
        updateConnectionState()

        if config.volatile_settings["_connected"] == "1":
            self.ui.pushButton_connection.setText("connected!")
            self.ui.pushButton_connection.setDisabled(True)

        else:
            self.ui.pushButton_connection.setText("connection failed...")
            self.ui.pushButton_connection.setDisabled(True)
            self.timer.start(2000)

    def _restore_button(self) -> None:
        """restores pressability of the button after a fail"""
        self.timer.stop()
        self.ui.pushButton_connection.setText("connect")
        self.ui.pushButton_connection.setDisabled(False)

    def saveSettings(self) -> None:
        config.general_settings[Configs.DB]["host"]      = self.ui.lineEdit_adress.text()
        config.general_settings[Configs.DB]["user"]      = self.ui.lineEdit_un.text()
        config.general_settings[Configs.DB]["password"]  = self.ui.lineEdit_pw.text()
        config.general_settings[Configs.DB]["port"]      = self.ui.lineEdit_port.text()
        config.general_settings[Configs.DB]["database"]  = self.ui.lineEdit_db.text()
