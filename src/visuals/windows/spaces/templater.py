"""the wrapper class for a single instance of plot spaces"""
from __future__ import annotations

import time
from loguru import logger
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget
from src.visuals.ui.generated.ui_NeoDiagrams import Ui_NeoDiagrams
from src.core.analyse.plugin import ApplyTemplate

from src.core.analyse.plotting import buildAnalyticsFigure

class NeoDiagrams(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.ui = Ui_NeoDiagrams()
        self.ui.setupUi(self)

        # init label
        self._init_windows()

        self.ui.checkBox_json.stateChanged.connect(self._change_avail)
        self.ui.checkBox_sql.stateChanged.connect(self._change_avail)
        self.ui.commandLink_plot.pressed.connect(self._execute_plot)


    def _init_windows(self):

        self.ui.commandLink_plot.setDisabled(True)
        self.ui.toolButton_sql.setDisabled(True)
        self.ui.comboBox_sql.setDisabled(True)
        self.ui.lineEdit_sql.setDisabled(True)
        self.ui.lineEdit_json.setDisabled(True)

    def _change_avail(self):

        jsonChecked = self.ui.checkBox_json.isChecked()
        self.ui.lineEdit_json.setDisabled(not jsonChecked)

        sqlChecked = self.ui.checkBox_sql.isChecked()
        self.ui.lineEdit_sql.setDisabled(not sqlChecked)
        self.ui.toolButton_sql.setDisabled(not sqlChecked)

        applyabel = (jsonChecked != sqlChecked)
        self.ui.commandLink_plot.setDisabled(not applyabel)

    def _execute_plot(self):

        sqlChecked = self.ui.checkBox_sql.isChecked()
        comboed = self.ui.comboBox_sql.currentText() != ""
        jsonChecked = self.ui.checkBox_json.isChecked()

        if comboed:
            pass

        if jsonChecked:
            ApplyTemplate(self.ui.lineEdit_json.text())
            self.ui.picture_root.setPixmap(QPixmap("gamefiles/test.png"))






class AnalyticsSingleton(QWidget):
    """the wrapper class for a analyticssingleton
    
    Attributes
    ----------
    ui : Ui_DiagramGenerator
        raw class produced by compilation
    pic : QPixmap
        the picture container for the figures
    _load_analytics : function
        starts the plotting process
    _reset_analytics : function
        clears the pixmap container
    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.ui = Ui_DiagramGenerator()
        self.ui.setupUi(self)

        # init label
        self.pic = QPixmap()
        self.ui.image_label.setPixmap(self.pic)

        # hooks for buttons
        self.ui.show_button.clicked.connect(self._load_analytics)
        self.ui.del_button.clicked.connect(self._reset_analytics)


    def _load_analytics(self) -> None:
        logger.trace("Loading a figure for the specified data.")
        player = self.ui.summoner_edit.text()
        mode = self.ui.prop_choose.currentText()
        diagram = self.ui.diagram_choose.currentText()
        current_width = self.ui.image_label.width()
        buildAnalyticsFigure(player, mode, (current_width, 400), diagram)
        self.pic = QPixmap(f"gamefiles/{mode}_{player}_{diagram}.png")
        self.ui.image_label.setPixmap(self.pic)
        logger.debug("Successfully loaded a figure, based on data.")


    def _reset_analytics(self) -> None:
        logger.trace("plot container cleared.")
        self.ui.image_label.clear()