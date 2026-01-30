"""the wrapper class for the window, which manages the LoadingScreenDialog."""
from __future__ import annotations

from loguru import logger
import time

from src.visuals.ui.generated.ui_loading import Ui_LoadingDialog

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QDialog, QApplication

class LoadingDialog(QDialog):
    """Wrapper class for the general settings window
    
    Attributes
    ----------
    ui : Ui_LoadingDialog
        the raw class, produced by compilation
    abs : int
        the absolute number of tasks
    done_i : int 
        the absolute number of finished tasks
    loading_state : int
        the relative frequency for printing into the screen

    """
    def __init__(self, parent, loaded_func, list_of_args: list[dict]) -> None:
        super().__init__(parent)
        logger.trace("Startet the LoadingsScreen Widget.")
        self.ui = Ui_LoadingDialog()
        self.ui.setupUi(self)
        
        self.abs: int = len(list_of_args)
        self.done_i: int = 0
        self.loading_state: int = 0
        self.ui.progressBar.setValue(0)

        # hooks for functionality
        QTimer.singleShot(30, lambda: self._execute_function(loaded_func, list_of_args))

    def _execute_function(self, loaded_func, list_of_args: list[dict]):
        """
        executes the function along a list of kwargs

        Parameters
        ----------
        loaded_func : function
            the function which is executed
        list_of_args : list[dict]
            a list of kwargs

        """
        logger.debug("Starting the executeprocess of the LoadingScreen.")
        for arg in list_of_args:
            logger.trace(f"Currently in executing the function {loaded_func} with the arg {arg}.")
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
        logger.debug("Successfully finished the executeprocess of the LoadingScreen.")
        QTimer.singleShot(2000,lambda: self.close())
            