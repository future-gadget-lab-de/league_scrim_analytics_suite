"""The wrapper class for handling the mariadb settings Dialog."""
from __future__ import annotations

from loguru import logger
import time
import numpy as np

from src.core.apis.riot import getEqualDistGameSamples, getMaxPageNumber
from src.core.io.mariadb import updateConnectionState
from src.core.config import config, Configs, locPathSet_c

from src.visuals.ui.generated.ui_sampledialog import Ui_Sampledialog
from src.visuals.windows.loading_dialog import LoadingDialog

from src.utils.io import writeSettingsFile

from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtCore import QTimer

class SampleDialog(QDialog):
    """Wrapper class for the mariadb settings window
    
    Attributes
    ----------
    ui : Ui_Dialog
        the raw sampledialog Class, produced by compilation
    """
    def __init__(self, parent=None) -> None:
        
        super().__init__(parent)
        self.ui = Ui_Sampledialog()
        self.ui.setupUi(self)

        # if execute button is clicked, execute that
        self.ui.commandLinkButton_sample.pressed.connect(self._execute_sample)


    def _execute_sample(self) -> None:
        """
        executes sampling for the provided settings
        """
        self.ui.commandLinkButton_sample.setDisabled(True)
        self.ui.buttonBox.setDisabled(True)
        QApplication.processEvents()
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

        QTimer.singleShot(2000,lambda: self.close())
