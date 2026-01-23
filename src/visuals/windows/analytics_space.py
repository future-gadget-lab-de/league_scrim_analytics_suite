"""the wrapper class which manages the container of the Analyticsspaces."""
from __future__ import annotations
from loguru import logger

from PySide6.QtWidgets import QWidget
from src.visuals.windows.analytics_singleton import AnalyticsSingleton
from src.visuals.ui.generated.ui_scroll_wrapper import Ui_Scroll_wrapper

class AnalyticsSpace(QWidget):
    """wrapper class for analyticsspaces
    
    Attributes
    ----------
    ui : Ui_Scroll_wrapper
        the raw Class, produced by compilation
    instances : list[AnalyticsSingleton]
        a list of analyticssingleton. used for managing them

    _remove_instance : function
        removes a instance of the Analyticssingleton
    _add_instance : function
        adding a instance of the Analyticssingleton
        
    """
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
        logger.trace("removed a Analyticssingleton instance.")

    def _add_instance(self) -> None:
        newInstance = AnalyticsSingleton()
        self.instances.append(newInstance)
        self.ui.scrollarea_insertlayout.addWidget(newInstance)
        logger.trace("added a Analyticssingleton instance.")
