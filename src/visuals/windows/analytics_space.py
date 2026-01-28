"""the wrapper class which manages the container of the Analyticsspaces."""
from __future__ import annotations
from loguru import logger

from src.visuals.windows.analytics_singleton import AnalyticsSingleton
from src.visuals.ui.generated.ui_scroll_wrapper import Ui_Scroll_wrapper

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout, QSizePolicy, QVBoxLayout, 
    QWidget, QSplitter, QLabel, QGroupBox, QPushButton)

class NeoAnalyticsSpace(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)

        horizontallayout = QHBoxLayout(self)

        self.splitter = QSplitter()
        self.splitter.addWidget(self._make_panel())


        horizontallayout.addWidget(self.splitter)
        self.setLayout(horizontallayout)


    def _make_panel(self) -> QGroupBox:
        group = QGroupBox()
        layout = QHBoxLayout()
        but1 = QPushButton("vert")
        but2 = QPushButton("hort")
        layout.addWidget(but1)
        layout.addWidget(but2)
        group.setLayout(layout)
        but1.clicked.connect(lambda checked=False, b=but1: self._add_Splitter(b, Qt.Orientation.Vertical, checked))
        but2.clicked.connect(lambda checked=False, b=but2: self._add_Splitter(b, Qt.Orientation.Horizontal, checked))
        return group

    
    def _add_Splitter(self, button: QPushButton, direction: Qt.Orientation, _checked: bool = False):
        widget = button.parent()
        splitter = widget.parent()

        if not isinstance(splitter, QSplitter):
            return
        splitter_ori = splitter.orientation()

        if direction == splitter_ori:
            splitter.addWidget(self._make_panel())
            return

        index = splitter.indexOf(widget)
        if index < 0:
            return
        old_widget = splitter.widget(index)
        if old_widget is None:
            return
        old_widget.setParent(None)
        newSplitter = QSplitter(orientation=direction)
        splitter.insertWidget(index, newSplitter)
        newSplitter.addWidget(old_widget)
        newSplitter.addWidget(self._make_panel())
        #newSplitter.setSizes([1, 1])
        

    def _divide_active_window(self):
        pass


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
        self.thinker = NeoAnalyticsSpace(self)
        # initializing a list of singletons, for proper management
        self.instances = list[AnalyticsSingleton]()
        self.ui.scrollarea_insertlayout.addWidget(self.thinker)



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
