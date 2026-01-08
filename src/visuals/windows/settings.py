from __future__ import annotations

from PySide6.QtWidgets import QDialog
from src.visuals.ui.generated.ui_settings import Ui_settings_dialog
from src.utils import readSettingsFile
from src.config import locPath_c
import logging
logger = logging.getLogger(__name__)

#NOTE: Wiso sind manche methods lower_lower_lower und manche lower_Upper...
class SettingsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_settings_dialog()
        self.ui.setupUi(self)
        
        settings_loc = readSettingsFile(locPath_c)
        self.settings = readSettingsFile(settings_loc["lsas"])
        self.init_fields()

        self.ui.lineEdit_csv_path.textChanged.connect(self.change_line_setting)
        self.ui.lineEdit_API.textChanged.connect(self.change_line_setting)
        self.ui.checkbox_mariadb_activated.stateChanged.connect(self.change_maria_setting)
        self.ui.checkBox_old_patch.stateChanged.connect(self.change_Legacy_Support)

    def init_fields(self) -> None:
        logger.trace("Start init_fields function for object: "+str(self))
        if self.settings["mariadb"] == "1":
            self.ui.checkbox_mariadb_activated.setChecked(True)
            self.ui.lineEdit_csv_path.setDisabled(True)
        if self.settings["old_patch_support"] == "1":
            self.ui.checkBox_old_patch.setChecked(True)
        self.ui.lineEdit_csv_path.setText(self.settings["csv_directory"])
        self.ui.lineEdit_API.setText(self.settings["API_key"])
        logger.trace("Finished init_fields function.")

    def get_settings(self) -> dict:
        logger.trace("Started get_settings for " + str(self))
        return self.settings

    def change_maria_setting(self) -> None:
        logger.trace("Started change_maria_setting function for object: " + str(self))
        if self.ui.checkbox_mariadb_activated.isChecked():
            self.settings["mariadb"] = "1"
            self.ui.lineEdit_csv_path.setDisabled(True)
            logger.debug("Enabled mariadb")
        else:
            self.settings["mariadb"] = "0"
            self.ui.lineEdit_csv_path.setEnabled(True)
            logger.debug("Disabled mariadb")
        logger.trace("Finished change_maria_setting function")

    def change_Legacy_Support(self):
        logger.trace("Started change_Legacy_Support function for object: " + str(self))
        if self.ui.checkBox_old_patch.isChecked():
            self.settings["old_patch_support"] = "1"
            logger.debug("Set old_patch_support to true")
        else:
            self.settings["old_patch_support"] = "0"
            logger.debug("Set old_patch_support to false")
        logger.trace("Finished change_Legacy_Support function.")

    def change_line_setting(self) -> None:
        logger.trace("Started change_line_setting function for object" + self)
        self.settings["csv_directory"] = self.ui.lineEdit_csv_path.text()
        self.settings["API_key"] = self.ui.lineEdit_API.text()
        logger.debug("Changed csv_directory setting to" +str(self.ui.lineEdit_csv_path) )
        logger.debug("Changed API_key setting to " + str(self.ui.lineEdit_API) )
        logger.trace("Finished change_line_setting function.")
