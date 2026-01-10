from __future__ import annotations

from PySide6.QtWidgets import QDialog
from src.visuals.ui.generated.ui_settings import Ui_settings_dialog

from src.config import readSettings,readInternalSettings, settings_list_c
from loguru import logger


#NOTE: Wiso sind manche methods lower_lower_lower und manche lower_Upper...
class SettingsDialog(QDialog):
    """Wrapper class for the general settings window"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_settings_dialog()
        self.ui.setupUi(self)
        
        # init settings
        self.lsas_settings = readSettings(settings_list_c[0])
        self.int_settings = readInternalSettings()
        self._init_fields()

        # hooks for functionality
        self.ui.lineEdit_csv_path.textChanged.connect(self._change_line_setting)
        self.ui.lineEdit_API.textChanged.connect(self._change_line_setting)
        self.ui.checkbox_mariadb_activated.stateChanged.connect(self._change_maria_setting)
        self.ui.checkBox_old_patch.stateChanged.connect(self._change_legacy_support)
        self.ui.comboBox_imported.currentIndexChanged.connect(self._change_label)

    def _init_fields(self) -> None:
        """initializes the settings fields with the current values of lsas.conf"""

        logger.trace("Start init_fields function for object: "+str(self))
        if self.lsas_settings["import_label"] == "date":
            self.ui.comboBox_imported.setCurrentIndex(1)
        if self.lsas_settings["mariadb"] == "1":
            self.ui.checkbox_mariadb_activated.setChecked(True)
            self.ui.lineEdit_csv_path.setDisabled(True)
        if self.lsas_settings["old_patch_support"] == "1":
            self.ui.checkBox_old_patch.setChecked(True)
        if self.int_settings["_connected"] == "0":
            self.ui.checkbox_mariadb_activated.setDisabled(True)
        self.ui.lineEdit_csv_path.setText(self.lsas_settings["csv_directory"])
        self.ui.lineEdit_API.setText(self.lsas_settings["API_key"])
        logger.trace("Finished init_fields function.")

    def _get_settings(self) -> dict:
        """returns the settings, for later use in mainWindow"""
        logger.trace("Started get_settings for " + str(self))
        return self.lsas_settings

    def _change_maria_setting(self) -> None:
        """Update the settings/window according to changed settings"""
        logger.trace("Started change_maria_setting function for object: " + str(self))
        if self.ui.checkbox_mariadb_activated.isChecked():
            self.lsas_settings["mariadb"] = "1"
            self.ui.lineEdit_csv_path.setDisabled(True)
            logger.debug("Enabled mariadb")
        else:
            self.lsas_settings["mariadb"] = "0"
            self.ui.lineEdit_csv_path.setEnabled(True)
            logger.debug("Disabled mariadb")
        logger.trace("Finished change_maria_setting function")

    def _change_legacy_support(self):
        """Update the settings/window according to changed settings"""
        logger.trace("Started change_Legacy_Support function for object: " + str(self))
        if self.ui.checkBox_old_patch.isChecked():
            self.lsas_settings["old_patch_support"] = "1"
            logger.debug("Set old_patch_support to true")
        else:
            self.lsas_settings["old_patch_support"] = "0"
            logger.debug("Set old_patch_support to false")
        logger.trace("Finished change_Legacy_Support function.")

    def _change_line_setting(self) -> None:
        """Update the settings/window according to changed settings"""
        logger.trace("Started change_line_setting function for object" + self)
        self.lsas_settings["csv_directory"] = self.ui.lineEdit_csv_path.text()
        self.lsas_settings["API_key"] = self.ui.lineEdit_API.text()
        logger.debug("Changed csv_directory setting to" +str(self.ui.lineEdit_csv_path) )
        logger.debug("Changed API_key setting to " + str(self.ui.lineEdit_API) )
        logger.trace("Finished change_line_setting function.")

    def _change_label(self) -> None:
        self.lsas_settings["import_label"] = self.ui.comboBox_imported.currentText()
