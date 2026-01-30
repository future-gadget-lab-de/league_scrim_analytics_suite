"""the wrapper class which manages the container of the Analyticsspaces."""
from __future__ import annotations
from loguru import logger
import json

from src.visuals.windows.spaces.templater import NeoDiagrams
from src.visuals.ui.generated.ui_scroll_wrapper import Ui_Scroll_wrapper
from src.core.config import locPathSet_c, config, Configs

from PySide6.QtCore import Qt, QKeyCombination, Signal
from PySide6.QtGui import QKeyEvent

from PySide6.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout, QSizePolicy, QVBoxLayout, 
    QWidget, QSplitter, QLabel, QGroupBox, QPushButton, QLineEdit)

from src.utils.io import writeJsonFile, readJsonFile

class NeoAnalyticsSingleton(QWidget):
    
    buttonpressed = Signal(str, QWidget)
    
    def __init__(self, contained: QWidget, parent=None):

        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        layout = QHBoxLayout(self)
        self.widget = contained
        layout.addWidget(self.widget)
        self.setLayout(layout)




    def keyPressEvent(self, e: QKeyEvent):

        mod = Qt.KeyboardModifier.ShiftModifier
        print(e.modifiers())

        if e.modifiers() == mod:
        
            match e.key():

                case Qt.Key.Key_H:
                    print("emitted")
                    self.buttonpressed.emit("horizontal", self)

                case Qt.Key.Key_V:
                    print("emitted")
                    self.buttonpressed.emit("vertical", self)

        super().keyPressEvent(e)

    def mousePressEvent(self, event):

        self.setFocus()
        super().mousePressEvent(event)

class NeoAnalyticsSpace(QWidget):
    def __init__(
        self, 
        parent=None, 
        recstruct: dict = [{
            "id": "rootpanel",
            "parent": "root"
        }]):

        super().__init__(parent)

        self.widgets = []
        self.splitter = []

        self.struct = dict()

        split = self._build_by_struct(recstruct, "root", 1, [])

        self.splitter.append(
            split
        )

        horizontallayout = QHBoxLayout(self)

        horizontallayout.addWidget(split)
        self.setLayout(horizontallayout)


    def _make_panel(self) -> NeoDiagrams:

        
        se = NeoDiagrams(ids=f"id_{len(self.widgets)}")
        test = NeoAnalyticsSingleton(se)



        se.ui.commandLink_plot.pressed.connect(self.saveStates)
        test.buttonpressed.connect(self._add_Splitter_str)

        #but1.clicked.connect(lambda checked=False, b=but1: self._add_Splitter(b, Qt.Orientation.Vertical, checked))
        #but2.clicked.connect(lambda checked=False, b=but2: self._add_Splitter(b, Qt.Orientation.Horizontal, checked))
        return test

    def _build_by_struct(self, rec_dict: list[dict], splitid: str, ind: int, size: list[int]):

        if ind%2 == 1:
            split = QSplitter(orientation=Qt.Orientation.Vertical)
        else:
            split = QSplitter(orientation=Qt.Orientation.Horizontal)
        
        self.splitter.append(split)
        split.setProperty("id", splitid)
        self.struct[splitid] = dict()
        self.struct[splitid]["children"] = []

        for widget in rec_dict:
            cid = widget["id"]
            self.struct[cid] = dict()

            if "children" in widget:
                re_split = self._build_by_struct(widget["children"], cid, ind+1, widget["size"])
                split.addWidget(re_split)
            else:
                newPanel = self._make_panel()
                newPanel.setProperty("id", cid)
                self.widgets.append(newPanel)
                split.addWidget(newPanel)

            self.struct[splitid]["children"].append(cid)
            self.struct[cid]["parent"] = splitid


        if size:
            split.setSizes(size)

        return split






    def saveStates(self):
        for widget in self.widgets:
            pass # get some and save

        for split in self.splitter:
            sid = split.property("id")
            sizes = split.sizes()
            self.struct[sid]["size"] = sizes

        baseids = self.struct["root"]["children"]
        rec_dict = self.recursifyDict(self.struct, baseids)
        print(rec_dict)
        writeJsonFile(rec_dict, locPathSet_c + "ctr.json")

    def recursifyDict(self, explicit: dict, ids: list[str]) -> dict:
        final = list()
        
        for i in ids:
            di = dict()
            di["id"] = i 
            for key in explicit[i]:
                di[key] = explicit[i][key]
            if "children" in explicit[i] and explicit[i]["children"] is not None:
                di["children"] = self.recursifyDict(explicit, explicit[i]["children"])
            
            final.append(di)
                

        return final

    def _add_Splitter_str(self, ident: str, wid: QWidget):
        if ident == "horizontal":
            direction = Qt.Orientation.Horizontal
        else: 
            direction = Qt.Orientation.Vertical

        widget = wid
        splitter: QSplitter = widget.parent()

        if not isinstance(splitter, QSplitter):
            return
        splitter_ori = splitter.orientation()
        widget_ind = splitter.indexOf(widget)

        len_of_struct = len(self.struct)

        if direction == splitter_ori:
            newpanel = self._make_panel()
            newpanel.setProperty("id", f"something_{len_of_struct}")
            print(self.struct[splitter.property("id")]["children"])
            print(newpanel.property("id"))

            self.struct[splitter.property("id")]["children"].append(newpanel.property("id"))
            self.struct[newpanel.property("id")] = dict()
            self.struct[newpanel.property("id")]["parent"] = splitter.property("id")
            self.widgets.append(newpanel)
            splitter.addWidget(newpanel)
            print(self.struct)
            return

        index = splitter.indexOf(widget)
        if index < 0:
            return
        old_widget = splitter.widget(index)
        if old_widget is None:
            return
        old_widget.setParent(None)
        newSplitter = QSplitter(orientation=direction)
        self.splitter.append(newSplitter)
        newSplitter.setProperty("id", f"sp_{len_of_struct}")
        splitter.insertWidget(index, newSplitter)
        newSplitter.addWidget(old_widget)
        new_widget = self._make_panel()
        self.widgets.append(new_widget)
        new_widget.setProperty("id", f"wi_{len_of_struct}")
        newSplitter.addWidget(new_widget)
        newSplitter.setSizes([1, 1])
        splitter.setSizes([1 for size in splitter.sizes()])
        print(widget.property("id"))
        self.struct[splitter.property("id")]["children"].remove(widget.property("id"))
        self.struct[splitter.property("id")]["children"].insert(index, newSplitter.property("id"))

        self.struct[newSplitter.property("id")] = dict()
        self.struct[newSplitter.property("id")]["parent"] = splitter.property("id")
        self.struct[newSplitter.property("id")]["children"] = [widget.property("id"), new_widget.property("id")]

        self.struct[widget.property("id")]["parent"] = newSplitter.property("id")

        self.struct[new_widget.property("id")] = dict()
        self.struct[new_widget.property("id")]["parent"] = newSplitter.property("id")

        print(self.struct)



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
        self.ui.scrollarea_insertlayout.addWidget(self.thinker)


        self.ui.toolButton_dell.clicked.connect(self.deleteLayout)
        self.ui.toolButton_loadl.clicked.connect(self.loadLayout)
        self.ui.toolButton_savel.clicked.connect(self.saveLayout)

    def saveLayout(self):
        self.thinker.saveStates()

    def loadLayout(self):
        path = locPathSet_c + "ctr.json"
        layout = readJsonFile(path)

        self.thinker.deleteLater()
        self.thinker = NeoAnalyticsSpace(self, layout)

        self.ui.scrollarea_insertlayout.addWidget(self.thinker)

    def deleteLayout(self):
        self.thinker.deleteLater()
        self.thinker = NeoAnalyticsSpace(self)

        self.ui.scrollarea_insertlayout.addWidget(self.thinker)

