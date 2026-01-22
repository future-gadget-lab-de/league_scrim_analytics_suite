from __future__ import annotations
from loguru import logger
import numpy as np

from PySide6.QtWidgets import QMainWindow, QFileDialog, QLabel
from src.visuals.ui.generated.ui_mainwindow import Ui_MainWindow
from src.visuals.windows.settings import SettingsDialog
from src.visuals.windows.maria_dialog import MariaDialog
from src.visuals.windows.analytics_space import AnalyticsSpace
from src.visuals.windows.loading_dialog import LoadingDialog

from src.core.process.reading import listImportedMatchfiles
from src.core.io.wrapper import executeSelectQuery
from src.core.io.mariadb import databaseSetup
from src.core.macros import importPipeline
from src.core.apis.riot import getEqualDistGameSamples, getMaxPageNumber
from src.utils.path import transformPathtoFileList
from src.utils.sqlquery import returnSelectQuery

from src.core.config import config, Configs
#TODO: Rewrite Logging
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.label_list: list[Qlabel] = []

        # setup the window
        self._update_window()

        # setup the analyticsworkspace
        self.space = AnalyticsSpace(self)
        self.ui.stackWorkspace.addWidget(self.space)

        # hooks for buttons/interaction
        self.ui.actionAdd_AnalyticsSpace.triggered.connect(self.space._add_instance)
        self.ui.actionRemove_AnalyticsSpace.triggered.connect(self.space._remove_instance)
        self.ui.button_sample.clicked.connect(self._execute_sample)
        self.ui.actionSettings_2.triggered.connect(self._open_settings)
        self.ui.actionMariaDB.triggered.connect(self._open_mariadb_config)
        self.ui.actionImport_Matchfile.triggered.connect(self._filedialog_opener)

    def _update_files(self) -> None:
        """method, which downstreams the gameids of imported files"""

        # delete old labels
        for label in self.label_list:
            label.deleteLater()
        self.label_list = list[QLabel]()

        labels = listImportedMatchfiles()

        for lab in labels:
            label = QLabel(text=lab)
            self.label_list.append(label)
            self.ui.scroll_sub_content.addWidget(label)
        logger.info("updated the list of imported Matchfiles.")

    def _update_window(self) -> None:
        """initialize the ui"""
        isV5Disabled = config.general_settings[Configs.MAIN]["V5"] == "0"
        self.ui.comboBox_division.setDisabled(isV5Disabled)
        self.ui.comboBox_queue.setDisabled(isV5Disabled)
        self.ui.comboBox_rank.setDisabled(isV5Disabled)
        self.ui.spin_sample.setDisabled(isV5Disabled)
        self.ui.button_sample.setDisabled(isV5Disabled)
        # load all included matches
        self._update_files()

    def _execute_sample(self) -> None:
        samplesize = self.ui.spin_sample.value()
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
            pass

        self._update_window()
    

    def _filedialog_opener(self) -> None:
        """method which controlls the fileopener window"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Matchfiles (*.json)")
        dialog.setViewMode(QFileDialog.Detail)
        dialog.selectFile("./")
        fileNames = None
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
        if fileNames is not None:
            ldlg = LoadingDialog(self, importPipeline, [{"pathToFolder": path} for path in fileNames])
            if ldlg.exec():
                pass
        self._update_window()

    def _open_settings(self) -> None:
        """helpermethod for handling settingsdialog"""
        dlg = SettingsDialog(self)
        if dlg.exec():  # True wenn accepted
            dlg.saveSettings()
            logger.info("general settings saved")
            
        self._update_window()

    def _open_mariadb_config(self) -> None:
        """helpermethod for handling mariadbdialog"""
        mdlg = MariaDialog(self)
        if mdlg.exec():
            mdlg._try_connection()
            logger.info("mariadb settings saved")

        self._update_window()
