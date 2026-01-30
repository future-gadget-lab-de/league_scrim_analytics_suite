"""The Wrapper Class for handling the settingsdialog."""

from __future__ import annotations

from PySide6.QtWidgets import QDialog
from src.visuals.ui.generated.ui_neosettings import Ui_settings_dialog
from src.visuals.windows.profile_dialog import ProfileDialog
from src.core.process.pipelines.client import labellistclient
from src.core.io.mariadb import databaseSetup
from src.core.process.manager import centralmanager
from src.core.meta import GameTable

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
    _start_profiles : function
        this starts the dialog, for creating a new profile
    _change_API : function
        function, which executes in order to update api fields
    _change_label : function
        function, which executes in order to update label fields
    _change_paths : function
        function, which executes in order to update path fields
    saveSettings : function
        saves the current settings to ram

    
    """
    def __init__(self, parent) -> None:

        super().__init__(parent)
        self.ui = Ui_settings_dialog()
        self.ui.setupUi(self)
        self._init_fields()
        logger.debug("Build the SettingsDialog Window")

        # hooks for functionality
        self.ui.checkBox_API.stateChanged.connect(self._change_API)
        self.ui.checkBox_imported.stateChanged.connect(self._change_label)
        self.ui.checkBox_paths.stateChanged.connect(self._change_paths)
        self.ui.pushButton_profile.clicked.connect(self._start_profiles)

    def _init_fields(self) -> None:
        logger.trace("Start init_fields function for object: "+str(self))
        list_of_profiles: list[str] = config.getFiles(Configs.PROF)
        self.ui.comboBox_profile.addItems(list_of_profiles)
        self.ui.comboBox_profile.setCurrentText(config.general_settings[Configs.MAIN]["current_prof"])

        csv = config.general_settings[Configs.MAIN]["csv_directory"]
        meta = config.general_settings[Configs.MAIN]["metadata_directory"]
        dir_dif = csv != "data" or meta != "meta"
        self.ui.checkBox_paths.setChecked(dir_dif)
        self.ui.lineEdit_csv.setText(csv)
        self.ui.lineEdit_meta.setText(meta)
        self.ui.lineEdit_csv.setDisabled(not dir_dif)
        self.ui.lineEdit_meta.setDisabled(not dir_dif)
        self.ui.toolButton_csv.setDisabled(not dir_dif)
        self.ui.toolButton_meta.setDisabled(not dir_dif)

        api = config.general_settings[Configs.MAIN]["API_key"]
        self.ui.checkBox_API.setChecked(bool(api))
        self.ui.lineEdit_API.setText(api)
        self.ui.lineEdit_API.setDisabled(not bool(api))

        label = config.general_settings[Configs.MAIN]["import_label"]
        self.ui.checkBox_imported.setChecked(bool(label))

        metacols = list(centralmanager.recent_tables[GameTable.META].iloc[0,:])
        if not label:
            self.ui.comboBox_imported.addItems([""])
        else:
            self.ui.comboBox_imported.addItems(metacols)

        self.ui.comboBox_imported.setCurrentText(label)

        logger.trace("Finished init_fields function.")

    def _start_profiles(self) -> None:
        dlg = ProfileDialog(self)
        if dlg.exec():
            dlg._add_prof()
        self.ui.comboBox_profile.clear()
        self.ui.comboBox_imported.clear()
        self._init_fields()

    def _change_API(self) -> None:

        logger.trace("Started change_maria_setting function for object: " + str(self))
        isChecked = self.ui.checkBox_API.isChecked()
        self.ui.lineEdit_API.setDisabled(not isChecked)
        if not isChecked:
            self.ui.lineEdit_API.setText("")
        logger.trace("Finished change_maria_setting function")

    def _change_label(self) -> None:
        self.ui.comboBox_imported.clear()
        logger.trace("Started change_maria_setting function for object: " + str(self))
        isChecked = self.ui.checkBox_imported.isChecked()
        self.ui.comboBox_imported.setDisabled(not isChecked)
        metacols = list(centralmanager.recent_tables[GameTable.META].iloc[0,:])
        if isChecked:
            self.ui.comboBox_imported.addItems(metacols)
        else:
            self.ui.comboBox_imported.addItems([""])
        logger.trace("Finished change_maria_setting function")

    def _change_paths(self) -> None:

        logger.trace("Started change_maria_setting function for object: " + str(self))
        isChecked = self.ui.checkBox_paths.isChecked()
        self.ui.lineEdit_csv.setDisabled(not isChecked)
        self.ui.lineEdit_meta.setDisabled(not isChecked)
        self.ui.toolButton_csv.setDisabled(not isChecked)
        self.ui.toolButton_meta.setDisabled(not isChecked)
        if not isChecked:
            self.ui.lineEdit_csv.setText("data")
            self.ui.lineEdit_meta.setText("meta")
        logger.trace("Finished change_maria_setting function")


    def saveSettings(self) -> None:
        
        config.general_settings[Configs.MAIN]["csv_directory"]      = self.ui.lineEdit_meta.text()
        config.general_settings[Configs.MAIN]["current_prof"]       = self.ui.comboBox_profile.currentText()
        config.general_settings[Configs.MAIN]["import_label"]       = self.ui.comboBox_imported.currentText()
        config.general_settings[Configs.MAIN]["API_key"]            = self.ui.lineEdit_API.text()
        config.general_settings[Configs.MAIN]["csv_directory"]      = self.ui.lineEdit_csv.text()

        config.setProfile(self.ui.comboBox_profile.currentText())
        centralmanager.updateManager()
        databaseSetup()

        logger.debug("Saved Settings via SettingsDialog to RAM.")

