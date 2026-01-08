from __future__ import annotations

import time

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QGraphicsView
from src.visuals.ui.generated.ui_diagram_generator import Ui_DiagramGenerator
from src.visuals.plotting import buildAnalyticsFigure, buildAnalyticsFigureBulk

from src.utils import readSettingsFile, writeSettingsFile
from src.config import locPath_c

class AnalyticsSingleton(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.ui = Ui_DiagramGenerator()
        self.ui.setupUi(self)

        self.pic = QPixmap()
        self.ui.image_label.setPixmap(self.pic)

        #self.ui.piclabel.clear()
        #picture = QGraphicsView("gamefiles/yo.png")

        self.settings_loc = readSettingsFile(locPath_c)
        self.settings = readSettingsFile(self.settings_loc["database"])
        self.initWindow()
        self.ui.show_button.clicked.connect(self.loadAnalytics)
        self.ui.del_button.clicked.connect(self.resetAnalytics)

    def initWindow(self):
        pass

    def loadAnalytics(self) -> None:
        player = self.ui.summoner_edit.text()
        mode = self.ui.prop_choose.currentText()
        diagram = self.ui.diagram_choose.currentText()
        current_width = self.ui.image_label.width()

        if diagram == "histo":
            buildAnalyticsFigureBulk(player, mode, (current_width, 400))
        else:
            buildAnalyticsFigure(player, mode, (current_width, 400))
        self.pic = QPixmap(f"gamefiles/{mode}_{player}.png")
        self.ui.image_label.setPixmap(self.pic)


    def resetAnalytics(self) -> None:
         self.ui.image_label.clear()