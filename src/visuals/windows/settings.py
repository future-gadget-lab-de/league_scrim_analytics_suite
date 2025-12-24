from __future__ import annotations

from PySide6.QtWidgets import QDialog
from src.visuals.ui.generated.ui_settings import Ui_settings_dialog

from src.utils import readSettingsFile

class SettingsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_settings_dialog()
        self.ui.setupUi(self)
        
        self.settings = readSettingsFile("config/lsas.conf")
        if self.settings["mariadb"] == "1":
            self.ui.checkbox_mariadb_activated.setChecked(True)
            self.ui.lineEdit_csv_path.setDisabled(True)
        self.ui.lineEdit_csv_path.setText(self.settings["csv_directory"])

        self.ui.lineEdit_csv_path.textChanged.connect(self.change_csv_setting)
        self.ui.checkbox_mariadb_activated.stateChanged.connect(self.change_maria_setting)

    def get_settings(self) -> dict:
        return self.settings

    def change_maria_setting(self) -> None:
        if self.ui.checkbox_mariadb_activated.isChecked():
            self.settings["mariadb"] = 1
            self.ui.lineEdit_csv_path.setDisabled(True)
        else:
            self.settings["mariadb"] = 0
            self.ui.lineEdit_csv_path.setEnabled(True)

    def change_csv_setting(self) -> None:
        self.settings["csv_directory"] = self.ui.lineEdit_csv_path.text()