from __future__ import annotations

import logging
logger = logging.getLogger(__name__)

from PySide6.QtWidgets import QMainWindow, QFileDialog, QCheckBox, QLabel
from src.visuals.ui.generated.ui_mainwindow import Ui_MainWindow
from src.visuals.windows.settings import SettingsDialog
from src.visuals.windows.maria_dialog import MariaDialog
from src.visuals.windows.analytics_space import AnalyticsSpace

from src.visuals.plotting import sqlDictToPandas

from src.database.queries import returnSelectQuery
from src.database.execution import buildConnection,executeQuery,getCursorSelect
from src.database.sqltemplates.template import importSQLQueries
from src.core.ops import importMatchfileData, clearData, databaseSetup

from src.utils import writeSettingsFile, readSettingsFile, getRelPath
from src.config import locPath_c

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.settings_loc = readSettingsFile(locPath_c)
        self.settings = readSettingsFile(self.settings_loc["lsas"])
        self.initMainWindow()

        self.space = AnalyticsSpace(self)
       
        self.ui.stackWorkspace.addWidget(self.space)

        self.updateFiles()

        # connect waiter
        self.ui.actionAdd_AnalyticsSpace.triggered.connect(self.space.addInstance)
        self.ui.actionRemove_AnalyticsSpace.triggered.connect(self.space.removeInstance)
        self.ui.button_execute.clicked.connect(self.execute_radio)
        self.ui.actionSettings_2.triggered.connect(self.open_settings)
        self.ui.actionMariaDB.triggered.connect(self.open_mariadb_config)
        self.ui.actionImport_Matchfile.triggered.connect(self.filedialog_opener)

    def initMainWindow(self) -> None:
        if self.settings["mariadb"] == "0":
            self.ui.radio_db_create.setDisabled(True)
            self.ui.actionMariaDB.setDisabled(True)

    def execute_radio(self) -> None:
        if self.ui.radio_db_create.isChecked():
            databaseSetup() 

    def filedialog_opener(self) -> None:
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Matchfiles (*.json)")
        dialog.setViewMode(QFileDialog.Detail)
        dialog.selectFile("./")
        if dialog.exec_():
            
            fileNames = dialog.selectedFiles()
            for file in fileNames:
                importMatchfileData(str(getRelPath(file)))
        #self.

    def updateFiles(self) -> None:

        query_date = returnSelectQuery("metadata",["gameid"])

        conn,cur = buildConnection()

        executeQuery([query_date], conn, cur)
        output_date = getCursorSelect(cur)

        conn.close()
        cur.close()

        data = sqlDictToPandas(output_date)

        for gameid in [str(gameid) for gameid in data["gameid"].values.tolist()]:
            self.ui.scroll_sub_content.addWidget(QLabel(text=gameid))


    def open_settings(self) -> None:
        dlg = SettingsDialog(self)
        if dlg.exec():  # True wenn accepted
            settings = dlg.get_settings()
            if settings["mariadb"] == "1":
                self.ui.radio_db_create.setDisabled(False)
                self.ui.actionMariaDB.setDisabled(False)
            else:
                self.ui.radio_db_create.setDisabled(True)
                self.ui.actionMariaDB.setDisabled(True)
            writeSettingsFile(settings, self.settings_loc["lsas"])
            logger.info("general settings saved")

    def open_mariadb_config(self) -> None:
        mdlg = MariaDialog(self)
        if mdlg.exec():
            settings = mdlg.get_settings()
            writeSettingsFile(settings, self.settings_loc["database"])
            logger.info("mariadb settings saved")
