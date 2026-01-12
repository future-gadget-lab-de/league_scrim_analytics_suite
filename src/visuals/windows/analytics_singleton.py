from __future__ import annotations

import time

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget
from src.visuals.ui.generated.ui_diagram_generator import Ui_DiagramGenerator
from src.visuals.plot.plotting import buildAnalyticsFigure

class AnalyticsSingleton(QWidget):
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
        player = self.ui.summoner_edit.text()
        mode = self.ui.prop_choose.currentText()
        diagram = self.ui.diagram_choose.currentText()
        current_width = self.ui.image_label.width()
        buildAnalyticsFigure(player, mode, (current_width, 400), diagram)
        self.pic = QPixmap(f"gamefiles/{mode}_{player}_{diagram}.png")
        self.ui.image_label.setPixmap(self.pic)


    def _reset_analytics(self) -> None:
        self.ui.image_label.clear()