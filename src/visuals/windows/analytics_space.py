from __future__ import annotations

from PySide6.QtWidgets import QWidget
from src.visuals.windows.analytics_singleton import AnalyticsSingleton
from src.visuals.ui.generated.ui_scroll_wrapper import Ui_Scroll_wrapper

class AnalyticsSpace(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Scroll_wrapper()
        self.ui.setupUi(self)

        # initializing a list of singletons, for proper management
        self.instances = list[AnalyticsSingleton]()

    def _remove_instance(self) -> None:
        self.ui.scrollarea_insertlayout.removeWidget(self.instances[-1])
        self.instances[-1].deleteLater()
        self.instances.pop()

    def _add_instance(self) -> None:
        newInstance = AnalyticsSingleton()
        self.instances.append(newInstance)
        self.ui.scrollarea_insertlayout.addWidget(newInstance)
