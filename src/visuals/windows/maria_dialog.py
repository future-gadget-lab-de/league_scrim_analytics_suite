from __future__ import annotations

import time

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer
from src.visuals.ui.generated.ui_maria_dialog import Ui_Dialog

from src.database.execution import updateConnectionState
from src.utils import readSettingsFile, writeSettingsFile
from src.config import locPath_c
class MariaDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.timer = QTimer(self)

        self.settings_loc = readSettingsFile(locPath_c)
        self.settings = readSettingsFile(self.settings_loc["database"])
        self.initWindow()


        self.timer.timeout.connect(self.restoreButton)
        self.ui.lineEdit_adress.textChanged.connect(self.change_setting)
        self.ui.lineEdit_db.textChanged.connect(self.change_setting)
        self.ui.lineEdit_port.textChanged.connect(self.change_setting)
        self.ui.lineEdit_pw.textChanged.connect(self.change_setting)
        self.ui.lineEdit_un.textChanged.connect(self.change_setting)
        self.ui.pushButton_connection.clicked.connect(self.tryConnection)

    def initWindow(self) -> None:
        if self.settings_loc["connected"] == "1":
            self.ui.pushButton_connection.setText("connected!")
            self.ui.pushButton_connection.setDisabled(True)

        self.ui.lineEdit_adress.setText(self.settings["host"])
        self.ui.lineEdit_db.setText(self.settings["database"])
        self.ui.lineEdit_port.setText(self.settings["port"])
        self.ui.lineEdit_pw.setText(self.settings["password"])
        self.ui.lineEdit_un.setText(self.settings["user"])

    def tryConnection(self) -> None:
        writeSettingsFile(self.settings, self.settings_loc["database"])
        updateConnectionState()
        self.settings_loc = readSettingsFile(locPath_c)
        if self.settings_loc["connected"] == "1":
            self.ui.pushButton_connection.setText("connected!")
            self.ui.pushButton_connection.setDisabled(True)
        else:
            self.ui.pushButton_connection.setText("connection failed...")
            self.ui.pushButton_connection.setDisabled(True)
            self.timer.start(2000)

    def restoreButton(self) -> None:
        self.timer.stop()
        self.ui.pushButton_connection.setText("connect")
        self.ui.pushButton_connection.setDisabled(False)

    def get_settings(self) -> dict:
        return self.settings

    def change_setting(self) -> None:
        if self.settings_loc["connected"] == "1":
            self.settings_loc["connected"] = "0"
            writeSettingsFile(self.settings_loc, locPath_c)
            self.restoreButton()

        self.settings["host"] = self.ui.lineEdit_adress.text()
        self.settings["database"] = self.ui.lineEdit_db.text()
        self.settings["port"] = self.ui.lineEdit_port.text()
        self.settings["password"] = self.ui.lineEdit_pw.text()
        self.settings["user"] = self.ui.lineEdit_un.text()
