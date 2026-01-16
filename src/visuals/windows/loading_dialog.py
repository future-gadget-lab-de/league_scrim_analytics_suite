from __future__ import annotations
import time

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QDialog, QApplication
from src.visuals.ui.generated.ui_loading import Ui_LoadingDialog

from src.config import readSettings,readInternalSettings, settings_list_c
from loguru import logger

class LoadingDialog(QDialog):
    """Wrapper class for the general settings window"""
    def __init__(self, parent, loaded_func, list_of_args: list) -> None:
        super().__init__(parent)
        self.ui = Ui_LoadingDialog()
        self.ui.setupUi(self)
        
        self.abs: int = len(list_of_args)
        self.done_i: int = 0
        self.loading_state: int = 0
        self.ui.progressBar.setValue(0)

        # hooks for functionality
        QTimer.singleShot(30, lambda: self._execute_function(loaded_func, list_of_args))

    def _execute_function(self, loaded_func, list_of_args):
        for arg in list_of_args:

            start = time.time()
            loaded_func(**arg)
            self.done_i += 1
            self.loading_state = int(100*(self.done_i / self.abs))
            self.ui.progressBar.setValue(self.loading_state)
            end = time.time()
            time_s_full = (end - start)*self.abs
            done_procent = 1 - (self.done_i / self.abs)
            time_left_in_s = round(time_s_full*done_procent)
            time_remaining = f"{time_left_in_s} s"
            if time_left_in_s > 60:
                time_left_in_min = round((time_left_in_s - (time_left_in_s % 60))/60)
                time_left_in_s = time_left_in_s - (time_left_in_min*60)
                time_remaining = f"{time_left_in_min} minutes and {time_left_in_s} seconds"
            
            self.ui.label_time.setText(f"{self.done_i}/{self.abs} - remaining time: {time_remaining}\n Attention: Do not close the window!")
            QApplication.processEvents()  # erzwingt UI-Updates
        self.ui.label_time.setText(f"done!")
        QTimer.singleShot(2000,lambda: self.close())
            