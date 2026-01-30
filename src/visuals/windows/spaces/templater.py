"""the wrapper class for a single instance of plot spaces"""
from __future__ import annotations

import time
from loguru import logger
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget
from src.visuals.ui.generated.ui_NeoDiagrams import Ui_NeoDiagrams
from src.core.analyse.plugin import ApplyTemplate, getPossiblePlots, executePlugin
from src.core.io.wrapper import executeSelectQuery

from src.core.analyse.plotting import buildAnalyticsFigure
from src.core.config import locPathSet_c, config, Configs

class NeoDiagrams(QWidget):

    def __init__(self, parent=None, ids: str = "") -> None:
        super().__init__(parent)

        self.id = ids
        self.ui = Ui_NeoDiagrams()
        self.ui.setupUi(self)

        # init label
        self._init_windows()

        self.ui.checkBox_json.stateChanged.connect(self._change_avail)
        self.ui.checkBox_sql.stateChanged.connect(self._change_avail)
        self.ui.commandLink_plot.pressed.connect(self._execute_plot)
        self.ui.toolButton_sql.pressed.connect(self._show_dropdown)


    def _init_windows(self):

        self.ui.commandLink_plot.setDisabled(True)
        self.ui.toolButton_sql.setDisabled(True)
        self.ui.comboBox_sql.setDisabled(True)
        self.ui.lineEdit_sql.setDisabled(True)
        self.ui.lineEdit_json.setDisabled(True)

    def _show_dropdown(self):

        query = self.ui.lineEdit_sql.text()

        results = getPossiblePlots([query])

        for res in results:
            print(list(res[0].keys()))
            self.ui.comboBox_sql.addItems([list(res[0].keys())[-1]])

        self._change_avail()


    def _change_avail(self):

        jsonChecked = self.ui.checkBox_json.isChecked()
        self.ui.lineEdit_json.setDisabled(not jsonChecked)

        if not jsonChecked:
            self.ui.lineEdit_json.setText("")

        sqlChecked = self.ui.checkBox_sql.isChecked()
        self.ui.lineEdit_sql.setDisabled(not sqlChecked)
        self.ui.toolButton_sql.setDisabled(not sqlChecked)

        if not sqlChecked:
            self.ui.lineEdit_sql.setText("")
            self.ui.comboBox_sql.clear()

        comboed = self.ui.comboBox_sql.currentText() != ""
        self.ui.comboBox_sql.setDisabled(not comboed)

        applyabel = (jsonChecked != sqlChecked)
        self.ui.commandLink_plot.setDisabled(not applyabel)

    def _execute_plot(self):

        sqlChecked = self.ui.checkBox_sql.isChecked()
        comboed = self.ui.comboBox_sql.currentText() != ""
        jsonChecked = self.ui.checkBox_json.isChecked()

        picpath = config.general_settings[Configs.MAIN]["metadata_directory"] \
                    + "/" + config.general_settings[Configs.MAIN]["current_prof"] \
                    + self.id + ".png"

        height = self.ui.groupBox.geometry().height()
        width = self.ui.groupBox.geometry().width()

        if comboed:
            DF = executeSelectQuery(self.ui.lineEdit_sql.text())
            executePlugin([DF], self.ui.comboBox_sql.currentText(), picpath, (width, height))
            self.ui.picture_root.setPixmap(QPixmap(picpath))

        if jsonChecked:
            ApplyTemplate(self.ui.lineEdit_json.text(), picpath, (width, height))
            self.ui.picture_root.setPixmap(QPixmap(picpath))

