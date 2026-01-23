"""The wrapper class for handling the mariadb settings Dialog."""

from __future__ import annotations

import time

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer
from src.visuals.ui.generated.ui_maria_dialog import Ui_Dialog

from src.core.io.mariadb import updateConnectionState
from src.core.config import config, Configs

class MariaDialog(QDialog):
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
        """MariaDialog Constructor"""
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        logger.debug("Build the SettingsDialog Window")
        self.timer = QTimer(self)
        logger.trace("Initialized the QTimer Class")

        # init settings
        self._init_fields()

        # try a connection
        self.timer.timeout.connect(self._restore_button)
        self.ui.pushButton_connection.clicked.connect(self._try_connection)

    def _init_fields(self) -> None:
        """initializes the current fields with values of mariadb.conf"""
        logger.trace("Start init_fields function for object: "+str(self))
        if config.volatile_settings["_connected"] == "1":
            self.ui.pushButton_connection.setText("connected!")
            self.ui.pushButton_connection.setDisabled(True)

        self.ui.lineEdit_adress.setText(config.general_settings[Configs.DB]["host"])
        self.ui.lineEdit_db.setText(config.general_settings[Configs.DB]["database"])
        self.ui.lineEdit_port.setText(config.general_settings[Configs.DB]["port"])
        self.ui.lineEdit_pw.setText(config.general_settings[Configs.DB]["password"])
        self.ui.lineEdit_un.setText(config.general_settings[Configs.DB]["user"])
        logger.trace("Finished init_fields function.")

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
            logger.trace("Started the QTimer for disabling the connection button.")

    def _restore_button(self) -> None:
        """restores pressability of the button after a fail"""
        self.timer.stop()
        self.ui.pushButton_connection.setText("connect")
        self.ui.pushButton_connection.setDisabled(False)
        logger.trace("Stopped the QTimer and Restored the Button to his original state.")

    def saveSettings(self) -> None:
        """saves values of GUI fields to RAM"""
        config.general_settings[Configs.DB]["host"]      = self.ui.lineEdit_adress.text()
        config.general_settings[Configs.DB]["user"]      = self.ui.lineEdit_un.text()
        config.general_settings[Configs.DB]["password"]  = self.ui.lineEdit_pw.text()
        config.general_settings[Configs.DB]["port"]      = self.ui.lineEdit_port.text()
        config.general_settings[Configs.DB]["database"]  = self.ui.lineEdit_db.text()
        logger.debug("Saved Settings via SettingsDialog to RAM.")
