from __future__ import annotations

import time

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QGraphicsView
#from src.visuals.ui.generated.ui_central_workspace import Ui_centralworkspace
from src.visuals.ui.generated.ui_central_workspace_Kopie import Ui_centralworkspace
from src.visuals.plotting import buildAnalyticsFigure

from src.utils import readSettingsFile, writeSettingsFile
from src.config import locPath_c

class AnalyticsSingleton(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.ui = Ui_centralworkspace()
        self.ui.setupUi(self)

        self.pic = QPixmap()
        self.ui.piclabel.setPixmap(self.pic)

        #self.ui.piclabel.clear()
        #picture = QGraphicsView("gamefiles/yo.png")

        self.settings_loc = readSettingsFile(locPath_c)
        self.settings = readSettingsFile(self.settings_loc["database"])
        self.initWindow()
        self.ui.pushButton.clicked.connect(self.loadAnalytics)
        self.ui.pushButton_2.clicked.connect(self.resetAnalytics)

    def initWindow(self):
        pass

    def loadAnalytics(self) -> None:
        player = self.ui.lineEdit.text()
        mode = self.ui.comboBox.currentText()

        buildAnalyticsFigure(player, mode, (self.ui.piclabel.width(), 400))

        self.pic = QPixmap(f"gamefiles/{mode}_{player}.png")
        self.ui.piclabel.setPixmap(self.pic)


    def resetAnalytics(self) -> None:
         self.ui.piclabel.clear()