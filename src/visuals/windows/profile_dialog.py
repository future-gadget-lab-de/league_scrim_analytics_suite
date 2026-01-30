"""The wrapper class for handling the mariadb settings Dialog."""
from __future__ import annotations

from loguru import logger
import time

from src.core.config import config, Configs, locPathSet_c, templates
from src.core.io.mariadb import updateConnectionState

from src.visuals.ui.generated.ui_profiles import Ui_Dialog

from src.utils.io import writeSettingsFile

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer

class ProfileDialog(QDialog):
    """Wrapper class for the mariadb settings window
    
    Attributes
    ----------
    ui : Ui_Dialog
        the raw MariaDialog Class, produced by compilation
    timer : QTimer
        a timer, which is used to count time for the connection button

    _init_fields : function
        initializes all fields with the provided values through
        the mariadbconfigs
    _try_connection : function
        gets activated, when the connection button is pressed. 
        Uses the QTimer, if a connection is not successful
    _restore_button : function
        restores the pressable buttonstate.
    saveSettings : function
        saves the current GUI Values to settings in RAM.
    
    """
    def __init__(self, parent=None) -> None:
        
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        logger.debug("Build the SettingsDialog Window")
        self.timer = QTimer(self)
        logger.trace("Initialized the QTimer Class")

        # init settings
        self._init_fields()

        self.ui.comboBox_filemode.currentIndexChanged.connect(self._change_con)

    def _init_fields(self) -> None:

        logger.trace("Start init_fields function for object: "+str(self))

        list_of_cons: list[str] = config.getFiles(Configs.DB)
        self.ui.comboBox_connection.addItems(list_of_cons)
        self.ui.comboBox_connection.addItem("")
        self.ui.comboBox_connection.setCurrentText("")
        self.ui.comboBox_connection.setDisabled(True)

        logger.trace("Finished init_fields function.")

    def _change_con(self) -> None:
        isDb = self.ui.comboBox_filemode.currentText() == "db"
        self.ui.comboBox_connection.setDisabled(not isDb)
        if not isDb:
            self.ui.comboBox_connection.setCurrentText("")


    def _add_prof(self) -> None:

        settings = templates[Configs.PROF]
        settings["mode"] = self.ui.comboBox_filemode.currentText()
        settings["con"] = self.ui.comboBox_connection.currentText()
        
        settings["format"] = self.ui.comboBox_gamefile.currentText()

        file = locPathSet_c + "profiles/" + self.ui.lineEdit_profilename.text() + ".conf"
        writeSettingsFile(settings, file)
