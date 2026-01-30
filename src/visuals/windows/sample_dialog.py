"""The wrapper class for handling the mariadb settings Dialog."""

from __future__ import annotations

import time
import numpy as np

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QTimer
from src.visuals.ui.generated.ui_sampledialog import Ui_Sampledialog
from src.core.apis.riot import getEqualDistGameSamples, getMaxPageNumber
from src.visuals.windows.loading_dialog import LoadingDialog

from loguru import logger
from src.core.io.mariadb import updateConnectionState
from src.utils.io import writeSettingsFile
from src.core.config import config, Configs, locPathSet_c

class SampleDialog(QDialog):
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
        self.ui = Ui_Sampledialog()
        self.ui.setupUi(self)
        logger.debug("Build the SettingsDialog Window")
        logger.trace("Initialized the QTimer Class")

        # try a connection
        self.ui.commandLinkButton_sample.pressed.connect(self._execute_sample)


    def _execute_sample(self) -> None:

        self.ui.commandLinkButton_sample.setDisabled(True)
        self.ui.buttonBox.setDisabled(True)

        samplesize = self.ui.spinBox_samplesize.value()
        logger.trace(f"Starting sampling {samplesize} gamefiles.")
        sample_vec = np.arange(samplesize)
        sample_list = list()

        pages_of_data = getMaxPageNumber(
            rank = self.ui.comboBox_rank.currentText(), 
            queue = self.ui.comboBox_queue.currentText(), 
            division = self.ui.comboBox_division.currentText()
        )
        for sample in sample_vec:
            sample_list.append(
                {
                    "rank": self.ui.comboBox_rank.currentText(),
                    "queue": self.ui.comboBox_queue.currentText(), 
                    "division": self.ui.comboBox_division.currentText(), 
                    "maxPageNumber": pages_of_data,
                    "samplesize": 1
                }
            )
        ldlg = LoadingDialog(self, getEqualDistGameSamples, sample_list)
        if ldlg.exec():
            logger.debug("LoadingDialog was running successful.")
            pass
