from __future__ import annotations
from loguru import logger


from PySide6.QtWidgets import QMainWindow, QFileDialog, QLabel
from src.visuals.ui.generated.ui_mainwindow import Ui_MainWindow
from src.visuals.windows.settings import SettingsDialog
from src.visuals.windows.maria_dialog import MariaDialog
from src.visuals.windows.analytics_space import AnalyticsSpace


from src.database.queries import returnSelectQuery
from src.database.wrapper import executeSelectQuery
from src.database.mariadb.execution import databaseSetup
from src.core.ops import importMatchfileData

from src.config import writeSettings, readSettings, writeInternalSettings, readInternalSettings, settings_list_c
#TODO: Rewrite Logging
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.settings_int = readInternalSettings()
        self.settings_lsas = readSettings(settings_list_c[0])
        self.label_list: list[Qlabel] = []

        # setup the window
        self._init_window()

        # setup the analyticsworkspace
        self.space = AnalyticsSpace(self)
        self.ui.stackWorkspace.addWidget(self.space)

        # hooks for buttons/interaction
        self.ui.actionAdd_AnalyticsSpace.triggered.connect(self.space._add_instance)
        self.ui.actionRemove_AnalyticsSpace.triggered.connect(self.space._remove_instance)
        self.ui.button_execute.clicked.connect(self._execute_radio)
        self.ui.actionSettings_2.triggered.connect(self._open_settings)
        self.ui.actionMariaDB.triggered.connect(self._open_mariadb_config)
        self.ui.actionImport_Matchfile.triggered.connect(self._filedialog_opener)

    def _init_window(self) -> None:
        """initialize the ui"""
        if self.settings_lsas["mariadb"] == "0":
            self.ui.radio_db_create.setDisabled(True)
        # load all included matches
        self._update_files()

    def _execute_radio(self) -> None:
        if self.ui.radio_db_create.isChecked():
            databaseSetup() 

    def _filedialog_opener(self) -> None:
        """method which controlls the fileopener window"""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Matchfiles (*.json)")
        dialog.setViewMode(QFileDialog.Detail)
        dialog.selectFile("./")
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            for file in fileNames:
                importMatchfileData(file)
        self._init_window()

    def _update_files(self) -> None:
        """method, which downstreams the gameids of imported files"""
        logger.info("updated imported stuff")

        # delete old labels
        for label in self.label_list:
            label.deleteLater()
        self.label_list = list[QLabel]()

        query = returnSelectQuery("metadata",[self.settings_lsas["import_label"]])
        data = executeSelectQuery(query)
        if data.empty:
            return 

        for gameid in [str(gameid) for gameid in data[self.settings_lsas["import_label"]].values.tolist()]:
            label = QLabel(text=gameid)
            self.label_list.append(label)
            self.ui.scroll_sub_content.addWidget(label)

    def _open_settings(self) -> None:
        """helpermethod for handling settingsdialog"""
        dlg = SettingsDialog(self)
        if dlg.exec():  # True wenn accepted
            settings = dlg._get_settings()
            self.settings_lsas = settings
            # update window
            writeSettings(settings_list_c[0], settings)
            logger.info("general settings saved")
        self._init_window()

    def _open_mariadb_config(self) -> None:
        """helpermethod for handling mariadbdialog"""
        mdlg = MariaDialog(self)
        if mdlg.exec():
            settings = mdlg._get_settings()
            # update window
            writeSettings(settings_list_c[1], settings)
            mdlg._try_connection()
            logger.info("mariadb settings saved")
        self._init_window()
