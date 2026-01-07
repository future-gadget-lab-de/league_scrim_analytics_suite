from __future__ import annotations

from PySide6.QtWidgets import QDialog
from src.visuals.ui.generated.ui_maria_dialog import Ui_Dialog

from src.utils import readSettingsFile
from src.config import locPath_c
class MariaDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        settings_loc = readSettingsFile(locPath_c)
        self.settings = readSettingsFile(settings_loc["database"])

        self.ui.lineEdit_adress.setText(self.settings["host"])
        self.ui.lineEdit_db.setText(self.settings["database"])
        self.ui.lineEdit_port.setText(self.settings["port"])
        self.ui.lineEdit_pw.setText(self.settings["password"])
        self.ui.lineEdit_un.setText(self.settings["user"])
        
        self.ui.lineEdit_adress.textChanged.connect(self.change_setting)
        self.ui.lineEdit_db.textChanged.connect(self.change_setting)
        self.ui.lineEdit_port.textChanged.connect(self.change_setting)
        self.ui.lineEdit_pw.textChanged.connect(self.change_setting)
        self.ui.lineEdit_un.textChanged.connect(self.change_setting)

    def get_settings(self) -> dict:
        return self.settings

    def change_setting(self) -> None: #Logging erfolgt in den einzelnen Methods
        self.settings["host"] = self.ui.lineEdit_adress.text()
        self.settings["database"] = self.ui.lineEdit_db.text()
        self.settings["port"] = self.ui.lineEdit_port.text()
        self.settings["password"] = self.ui.lineEdit_pw.text()
        self.settings["user"] = self.ui.lineEdit_un.text()
