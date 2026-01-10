from __future__ import annotations

import time

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer
from src.visuals.ui.generated.ui_maria_dialog import Ui_Dialog

from src.database.mariadb.execution import updateConnectionState
from src.config import readSettings, writeSettings, readInternalSettings, settings_list_c

class MariaDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.timer = QTimer(self)

        # init settings
        self.db_settings = readSettings(settings_list_c[1])
        self.int_settings = readInternalSettings()
        self._init_fields()

        # change callbacks
        self.ui.lineEdit_adress.textChanged.connect(self._change_setting)
        self.ui.lineEdit_db.textChanged.connect(self._change_setting)
        self.ui.lineEdit_port.textChanged.connect(self._change_setting)
        self.ui.lineEdit_pw.textChanged.connect(self._change_setting)
        self.ui.lineEdit_un.textChanged.connect(self._change_setting)

        # try a connection
        self.timer.timeout.connect(self._restore_button)
        self.ui.pushButton_connection.clicked.connect(self._try_connection)

    def _init_fields(self) -> None:
        """initializes the current fields with values of mariadb.conf"""
        if self.int_settings["_connected"] == "1":
            self.ui.pushButton_connection.setText("connected!")
            self.ui.pushButton_connection.setDisabled(True)

        self.ui.lineEdit_adress.setText(self.db_settings["host"])
        self.ui.lineEdit_db.setText(self.db_settings["database"])
        self.ui.lineEdit_port.setText(self.db_settings["port"])
        self.ui.lineEdit_pw.setText(self.db_settings["password"])
        self.ui.lineEdit_un.setText(self.db_settings["user"])

    def _try_connection(self) -> None:
        """connection test, which also writes settings according to the outcome"""
        writeSettings(settings_list_c[1], self.db_settings)
        self.int_settings["_connected"] = updateConnectionState()

        if self.int_settings["_connected"] == "1":
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

    def _get_settings(self) -> dict:
        return self.db_settings

    def _change_setting(self) -> None:
        """update window/settings according to the changed settings"""
        self._restore_button()
        self.db_settings["host"] = self.ui.lineEdit_adress.text()
        self.db_settings["database"] = self.ui.lineEdit_db.text()
        self.db_settings["port"] = self.ui.lineEdit_port.text()
        self.db_settings["password"] = self.ui.lineEdit_pw.text()
        self.db_settings["user"] = self.ui.lineEdit_un.text()
