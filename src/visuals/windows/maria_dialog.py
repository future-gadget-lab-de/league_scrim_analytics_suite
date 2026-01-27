"""The wrapper class for handling the mariadb settings Dialog."""

from __future__ import annotations

import time

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer
from src.visuals.ui.generated.ui_maria_dialog import Ui_Dialog

from loguru import logger
from src.core.io.mariadb import updateConnectionState
from src.utils.io import writeSettingsFile
from src.core.config import config, Configs, locPathSet_c

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
        self.ui.pushButton_add.clicked.connect(self._add_con)
        self.ui.checkBox_maria.stateChanged.connect(self._change_maria)

    def _init_fields(self) -> None:

        logger.trace("Start init_fields function for object: "+str(self))

        connections = bool(config.getFiles(Configs.DB))
        self.ui.checkBox_maria.setChecked(connections)
        self.ui.lineEdit_adress.setDisabled(not connections)
        self.ui.lineEdit_db.setDisabled(not connections)
        self.ui.lineEdit_port.setDisabled(not connections)
        self.ui.lineEdit_pw.setDisabled(not connections)
        self.ui.lineEdit_un.setDisabled(not connections)
        self.ui.lineEdit.setDisabled(not connections)
        self.ui.pushButton_add.setDisabled(True)
        self.ui.pushButton_connection.setDisabled(not connections)

        logger.trace("Finished init_fields function.")

    def _change_maria(self) -> None:

        logger.trace("Started change_maria_setting function for object: " + str(self))
        isChecked = self.ui.checkBox_maria.isChecked()
        self.ui.lineEdit_adress.setDisabled(not isChecked)
        self.ui.lineEdit_db.setDisabled(not isChecked)
        self.ui.lineEdit_port.setDisabled(not isChecked)
        self.ui.lineEdit_pw.setDisabled(not isChecked)
        self.ui.lineEdit_un.setDisabled(not isChecked)
        self.ui.lineEdit.setDisabled(not isChecked)
        self.ui.pushButton_add.setDisabled(True)
        self.ui.pushButton_connection.setDisabled(not isChecked)
        if not isChecked:
            self.ui.lineEdit_adress.setText("")
            self.ui.lineEdit.setText("")
            self.ui.lineEdit_db.setText("")
            self.ui.lineEdit_port.setText("")
            self.ui.lineEdit_pw.setText("")
            self.ui.lineEdit_un.setText("")
        logger.trace("Finished change_maria_setting function")

    def _add_con(self) -> None:

        settings = {
            "host": self.ui.lineEdit_adress.text(),
            "user": self.ui.lineEdit_un.text(),
            "password": self.ui.lineEdit_pw.text(),
            "port": self.ui.lineEdit_port.text(),
            "database": self.ui.lineEdit_db.text()
        }
        file = locPathSet_c + "connections/" + self.ui.lineEdit.text() + ".conf"
        writeSettingsFile(settings, file)
        self.ui.lineEdit_adress.setText("")
        self.ui.lineEdit.setText("")
        self.ui.lineEdit_db.setText("")
        self.ui.lineEdit_port.setText("")
        self.ui.lineEdit_pw.setText("")
        self.ui.lineEdit_un.setText("")
        self._restore_button()

    def _try_connection(self) -> None:

        updateConnectionState({
            "host": self.ui.lineEdit_adress.text(),
            "user": self.ui.lineEdit_un.text(),
            "password": self.ui.lineEdit_pw.text(),
            "port": self.ui.lineEdit_port.text(),
            "database": self.ui.lineEdit_db.text()
        })

        if config.volatile_settings["_connected"] == "1":
            self.ui.pushButton_connection.setText("connected!")
            self.ui.pushButton_connection.setDisabled(True)
            self.ui.pushButton_add.setDisabled(False)

        else:
            self.ui.pushButton_connection.setText("connection failed...")
            self.ui.pushButton_connection.setDisabled(True)
            self.timer.start(2000)
            logger.trace("Started the QTimer for disabling the connection button.")

    def _restore_button(self) -> None:

        self.timer.stop()
        self.ui.pushButton_connection.setText("connect")
        self.ui.pushButton_connection.setDisabled(False)
        self.ui.pushButton_add.setDisabled(True)
        logger.trace("Stopped the QTimer and Restored the Button to his original state.")

