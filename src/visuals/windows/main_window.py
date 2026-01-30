"""The Wrapper class for the main Window, which is started with the GUI."""
from __future__ import annotations
from loguru import logger
import numpy as np

from PySide6.QtWidgets import QMainWindow, QFileDialog, QLabel
from src.visuals.ui.generated.ui_mainwindow import Ui_MainWindow
from src.visuals.windows.settings import SettingsDialog
from src.visuals.windows.maria_dialog import MariaDialog
from src.visuals.windows.analytics_space import AnalyticsSpace
from src.visuals.windows.loading_dialog import LoadingDialog
from src.visuals.windows.sample_dialog import SampleDialog

from src.core.process.reading import listImportedMatchfiles
from src.core.io.wrapper import executeSelectQuery
from src.core.io.mariadb import databaseSetup
from src.core.macros import importPipeline
from src.core.apis.riot import getEqualDistGameSamples, getMaxPageNumber
from src.utils.path import transformPathtoFileList
from src.utils.sqlquery import returnSelectQuery
from src.core.meta import ImportType

from src.core.config import config, Configs
#TODO: Rewrite Logging
class MainWindow(QMainWindow):
    """Wrapper class for the Main Window
    
    Attributes
    ----------
    ui : Ui_MainWindow
        the raw MainWindow Class, produced by compilation
    label_list : list[QLabel]
        a list of label, which is used for keeping track of the 
        gameids already imported
    space : AnalyticsSpace
        An instance of the AnalyticsSpace class

    _update_window : function
        updates the MainWindow
    _update_files : function
        updates the list of QLables with the current imported Gamefiles
    _execute_sample : function
        downstreams a sample of gamefiles according to the 
        passed configuration in the MainWindow
    _filedialog_opener : function
        Handles the fileDialog, which is in use to import the gamefiles
    _open_settings : function
        creates an instance of a SettingsDialog
    _open_mariadb_config : function
        creates an instance of a MariaDialog

    """

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
        logger.debug("Setupped the AnalyticsSpace.")

        # hooks for buttons/interaction
        #self.ui.actionAdd_AnalyticsSpace.triggered.connect(self.space._add_instance)
        #self.ui.actionRemove_AnalyticsSpace.triggered.connect(self.space._remove_instance)
        #self.ui.button_sample.clicked.connect(self._execute_sample)
        self.ui.actionSample.triggered.connect(self._open_sample)
        self.ui.actionSettings_2.triggered.connect(self._open_settings)
        self.ui.actionMariaDB.triggered.connect(self._open_mariadb_config)
        self.ui.actionImport_Matchfile.triggered.connect(self._match_importer)
        self.ui.actionImport_Timeline.triggered.connect(self._time_importer)
        self.ui.actionImported_games_bar.triggered.connect(self._show_files)

    def _show_files(self) -> None:
        isChecked = self.ui.actionImported_games_bar.isChecked()

        self.ui.widget_import.setVisible(isChecked)

    def _update_files(self) -> None:

        logger.trace("Starting Updating the list of imported matchfiles.")
        # delete old labels
        for label in self.label_list:
            label.deleteLater()
        self.label_list = list[QLabel]()

        labels = listImportedMatchfiles()

        for lab in labels:
            label = QLabel(text=lab)
            self.label_list.append(label)
            self.ui.scroll_sub_content.addWidget(label)
        logger.debug("Adjusted the QLabels, which manages the imported matchfiles.")
        logger.trace("updated the list of imported Matchfiles.")

    def _update_window(self) -> None:

        logger.trace("Starting updating the GUI objects.")
        isV5 = config.general_settings[Configs.PROF]["format"] == "matchv5"
        self.ui.actionImported_games_bar.setChecked(True)
        self.ui.actionSample.setDisabled(not isV5)
        # self.ui.comboBox_division.setDisabled(isV5Disabled)
        # self.ui.comboBox_queue.setDisabled(isV5Disabled)
        # self.ui.comboBox_rank.setDisabled(isV5Disabled)
        # self.ui.spin_sample.setDisabled(isV5Disabled)
        # self.ui.button_sample.setDisabled(isV5Disabled)
        # load all included matches
        self._update_files()

    

    def _filedialog_opener(self) -> list[str] | None:

        logger.trace("Starting setup the FileDialog.")
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Matchfiles (*.json)")
        dialog.setViewMode(QFileDialog.Detail)
        dialog.selectFile("./")
        fileNames = None
        if dialog.exec_():
            logger.debug("successful run the FileDialog.")
            fileNames = dialog.selectedFiles()

        return fileNames

    def _match_importer(self) -> None:
        files = self._filedialog_opener()

        if files is not None:
            ldlg = LoadingDialog(self, importPipeline, [{"pathToFolder": path, "typ": ImportType.GENERAL} for path in files])
            if ldlg.exec():
                logger.debug("successful run the LoadingDialog.")
                pass
        self._update_window()


    def _time_importer(self) -> None:
        files = self._filedialog_opener()

        if files is not None:
            ldlg = LoadingDialog(self, importPipeline, [{"pathToFolder": path, "typ": ImportType.TIMELINE} for path in files])
            if ldlg.exec():
                logger.debug("successful run the LoadingDialog.")
                pass
        self._update_window()


    def _open_sample(self) -> None:
        dlg = SampleDialog()
        if dlg.exec():
            pass
        self._update_window()


    def _open_settings(self) -> None:

        logger.trace("Start building the SettingsDialog.")
        dlg = SettingsDialog(self)
        if dlg.exec():  # True wenn accepted
            dlg.saveSettings()
            logger.debug("Successfully run the SettingsDialog.")
            
        self._update_window()

    def _open_mariadb_config(self) -> None:
        
        logger.trace("Start building the MariaDialog.")
        mdlg = MariaDialog(self)
        if mdlg.exec():
            logger.debug("Successfully run the MariaDialog.")

        self._update_window()
