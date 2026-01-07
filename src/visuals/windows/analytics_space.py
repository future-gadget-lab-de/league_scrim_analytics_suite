from __future__ import annotations

import time

from PySide6.QtWidgets import QWidget
from src.visuals.windows.analytics_singleton import AnalyticsSingleton
from src.visuals.ui.generated.ui_central_scrollcontainer import Ui_Form

from src.utils import readSettingsFile, writeSettingsFile
from src.config import locPath_c

class AnalyticsSpace(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)


        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.instances = list[AnalyticsSingleton]()

        self.settings_loc = readSettingsFile(locPath_c)
        self.settings = readSettingsFile(self.settings_loc["database"])
        self.initWindow()

    def removeInstance(self) -> None:
        self.ui.scrollarea_insertlayout.removeWidget(self.instances[-1])
        self.instances[-1].deleteLater()
        self.instances.pop()

    def addInstance(self) -> None:
        newInstance = AnalyticsSingleton()
        self.instances.append(newInstance)
        self.ui.scrollarea_insertlayout.addWidget(newInstance)

    def initWindow(self):
        pass