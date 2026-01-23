"""The Wrapper Class for handling the settingsdialog."""

from __future__ import annotations

from PySide6.QtWidgets import QDialog
from src.visuals.ui.generated.ui_settings import Ui_settings_dialog

from src.core.config import config, Configs
from loguru import logger

class SettingsDialog(QDialog):
    """Wrapper class for the general settings window
    
    Attributes
    ----------
    ui : Ui_settings_dialog
        the raw SettingsDialog Class, produced by compilation

    _init_fields : function
        initializes all fields with the provided values through
        the configs
    _change_maria_setting : function
        gets activated, whe the mariadb checkbox toggles. 
        enables or disables the csv path option.
    saveSettings : function
        saves the current GUI Values to settings in RAM.
    
    """
    def __init__(self, parent) -> None:
        """SettingsDialog Constructor"""
        super().__init__(parent)
        self.ui = Ui_settings_dialog()
        self.ui.setupUi(self)
        self._init_fields()
        logger.debug("Build the SettingsDialog Window")

        # hooks for functionality
        self.ui.checkbox_mariadb_activated.stateChanged.connect(self._change_maria_setting)

    def _init_fields(self) -> None:
        """initializes the settings fields with the current values of lsas.conf"""

        logger.trace("Start init_fields function for object: "+str(self))
        if config.general_settings[Configs.MAIN]["import_label"] == "date":
            self.ui.comboBox_imported.setCurrentIndex(1)
        if config.general_settings[Configs.MAIN]["mariadb"] == "1":
            self.ui.checkbox_mariadb_activated.setChecked(True)
            self.ui.lineEdit_csv_path.setDisabled(True)
        if config.general_settings[Configs.MAIN]["V5"] == "1":
            self.ui.checkBox_V5.setChecked(True)
        if config.general_settings[Configs.MAIN]["old_patch_support"] == "1":
            self.ui.checkBox_old_patch.setChecked(True)
        if config.volatile_settings["_connected"] == "0":
            self.ui.checkbox_mariadb_activated.setDisabled(True)
        self.ui.lineEdit_csv_path.setText(config.general_settings[Configs.MAIN]["csv_directory"])
        self.ui.lineEdit_API.setText(config.general_settings[Configs.MAIN]["API_key"])
        logger.trace("Finished init_fields function.")

    def _change_maria_setting(self) -> None:
        """Update the settings/window according to changed settings"""
        logger.trace("Started change_maria_setting function for object: " + str(self))
        if self.ui.checkbox_mariadb_activated.isChecked():
            self.ui.lineEdit_csv_path.setDisabled(True)
            logger.debug("Enabled mariadb")
        else:
            self.ui.lineEdit_csv_path.setEnabled(True)
            logger.debug("Disabled mariadb")
        logger.trace("Finished change_maria_setting function")


    def saveSettings(self) -> None:
        """saves values of GUI fields to RAM"""
        config.general_settings[Configs.MAIN]["V5"]                 = str(int(self.ui.checkBox_V5.isChecked()))
        config.general_settings[Configs.MAIN]["mariadb"]            = str(int(self.ui.checkbox_mariadb_activated.isChecked()))
        config.general_settings[Configs.MAIN]["old_patch_support"]  = str(int(self.ui.checkBox_old_patch.isChecked()))
        config.general_settings[Configs.MAIN]["import_label"]       = self.ui.comboBox_imported.currentText()
        config.general_settings[Configs.MAIN]["API_key"]            = self.ui.lineEdit_API.text()
        config.general_settings[Configs.MAIN]["csv_directory"]      = self.ui.lineEdit_csv_path.text()
        logger.debug("Saved Settings via SettingsDialog to RAM.")

