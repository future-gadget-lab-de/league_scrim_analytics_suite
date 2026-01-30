"""custom class, which manages an i3 like tiling environment"""
from __future__ import annotations
from loguru import logger

from src.core.config import locPathSet_c, config, Configs

from src.visuals.windows.spaces.templater import NeoDiagrams
from src.visuals.ui.generated.ui_scroll_wrapper import Ui_Scroll_wrapper

from src.utils.io import writeJsonFile, readJsonFile

from PySide6.QtCore import Qt, QKeyCombination, Signal
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout, QSizePolicy, QVBoxLayout, 
    QWidget, QSplitter, QLabel, QGroupBox, QPushButton, QLineEdit)


class NeoAnalyticsSingleton(QWidget):
    """class for each field in the i3 like layout
    
    widget : QWidget
        the widget, that this tile contains
        
    """
    # signal, for processing the keycombinations in the AnalyticsSpace
    combinationNoticed = Signal(str, QWidget)
    
    def __init__(self, contained: QWidget, parent=None):

        super().__init__(parent)

        # attributes
        self.widget: QWidget = contained
        # setup visuals
        layout = QHBoxLayout(self)
        layout.addWidget(self.widget)
        self.setLayout(layout)
        # make the tile focusable
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def keyPressEvent(self, e: QKeyEvent):
        """
        overwritten keyPressEvent function, which activates, when a key
        is pressed for example.

        Parameters
        ----------
        e : QKeyEvent
            catches the Keyevents (presses, releases, ...)
        """
        # shift enum value
        mod: Qt.KeyboardModifier = Qt.KeyboardModifier.ShiftModifier

        # is shift pressed?
        if e.modifiers() == mod:

            # match if the key pressed is:
            match e.key():

                # H
                case Qt.Key.Key_H:
                    self.combinationNoticed.emit("horizontal", self)
                # V
                case Qt.Key.Key_V:
                    self.combinationNoticed.emit("vertical", self)

        # after custom activation continue with the inherited eventfunction
        super().keyPressEvent(e)

    def mousePressEvent(self, event: QMouseEvent):
        """
        overwritten mousePressEvent, which activates for example, if 
        a mouse button is pressed. used for highlighting tiles, since keypresses
        are only noticed on highlighted widgets

        Parameters
        ----------
        event
            catches the mousebuttonevents (presses, releases, ...)
        """
        self.setFocus()
        # continue with inherited function
        super().mousePressEvent(event)

class NeoAnalyticsSpace(QWidget):
    """An i3 like layout handler widget
    
    Attributes
    ----------
    widgets : list[QWidget]
        a list of all widgets, for accessing them efficiently
    splitter : list[QSplitter]
        the same concept, as in the widget case
    treetracker : dict[str, dict[str, list[str] | str]]
        keeps track of the tree structure, with adjacency lists
        id --> children: list[str]

    """
    def __init__(
        self, 
        parent=None, 
        tree: dict = [{
            "id": "rootpanel",
            "parent": "root"
        }]):

        super().__init__(parent)
        # attributes
        self.widgets: list[QWidget] = []
        self.splitter: list[QSplitter] = []
        self.treetracker: dict[str, dict[str, list[str] | str]] = dict()

        # initialize the tree structure
        initialSplitter: QSplitter = self._build_by_json_tree(tree, "root", 1, [])

        self.splitter.append(
            initialSplitter
        )
        # initialize the visuals
        horizontallayout = QHBoxLayout(self)
        horizontallayout.addWidget(initialSplitter)
        self.setLayout(horizontallayout)


    def _make_panel(self) -> NeoAnalyticsSingleton:
        """this method does make an instance of the widget, that gets pasted into the tiles"""
        
        uniqueId = f"id_{len(self.widgets)}"
        instanceOfWidget: NeoDiagrams = NeoDiagrams(ids=uniqueId)
        tileWrapper: NeoAnalyticsSingleton = NeoAnalyticsSingleton(instanceOfWidget)

        self.widgets.append(tileWrapper)

        instanceOfWidget.ui.commandLink_plot.pressed.connect(self._save_states)
        tileWrapper.combinationNoticed.connect(self._add_splitter)

        return tileWrapper

    def _build_by_json_tree(
        self, 
        childrenDicts: list[dict], 
        currentId: str, 
        altIndex: int, 
        splitterSizes: list[int]
        ) -> QSplitter:
        """recursive method, for initializing a jsontree, which was saved before
        
        Parameters
        ----------
        childrenDicts : list[dict]
            the metadicts for the children of the current splitter
        currentId : str
            the id of the current Splitter
        altIndex : int
            a raising indexnumber, which is used for the alternating split
            structure
        splitterSizes : list[int]
            used for setting the correct proportions for the splitter

        Returns
        -------
        currentSplitter : QSplitter
            returns the qsplitter int the current scope

        """
        # the structure is always alternating between vertical and horizontal
        if altIndex%2 == 1:
            currentSplitter: QSplitter = QSplitter(orientation=Qt.Orientation.Vertical)
        else:
            currentSplitter: QSplitter = QSplitter(orientation=Qt.Orientation.Horizontal)
        
        self.splitter.append(currentSplitter)

        # update property of widget
        currentSplitter.setProperty("id", currentId)

        # update the treetracker, for preventing keyerrors
        self.treetracker[currentId] = dict()
        self.treetracker[currentId]["children"] = []

        for childDict in childrenDicts:
            # read the id of the child
            childId: str = childDict["id"]
            self.treetracker[childId] = dict()
            isSplitterChild: bool = "children" in childDict

            if isSplitterChild:
                # if the child is a splitter, start the method again
                childSplitter: QSplitter = self._build_by_json_tree(
                    childDict["children"], 
                    childId, 
                    altIndex+1, 
                    childDict["size"]
                )
                currentSplitter.addWidget(childSplitter)
            else:
                # if the child is a widget, save it
                childWidget: NeoAnalyticsSingleton = self._make_panel()
                childWidget.setProperty("id", childId)
                currentSplitter.addWidget(childWidget)

            self.treetracker[currentId]["children"].append(childId)
            self.treetracker[childId]["parent"] = currentId

        if splitterSizes:
            # set sizes
            currentSplitter.setSizes(splitterSizes)

        return currentSplitter


    def _save_states(self):
        """ saves the current layout to the ctr.json in the config folder """

        # adjust tree tracker for all widgets
        for widgetInstances in self.widgets:
            pass # TODO: later expansion
        
        # adjust tree tracker for all splitter
        for splitterInstance in self.splitter:
            splitterId: str = splitterInstance.property("id")
            splitterSize: list[int] = splitterInstance.sizes()
            self.treetracker[splitterId]["size"] = splitterSize

        # get the start children from the constant root id
        RootChildrenIds: list[str] = self.treetracker["root"]["children"]
        # build the recursive variant of the tree tracker
        recursiveTreeTracker: dict = self._explicit_to_recursive_dict(self.treetracker, RootChildrenIds)
        # write the recursive variant to the ctr.json
        writeJsonFile(recursiveTreeTracker, locPathSet_c + "ctr.json")

    def _explicit_to_recursive_dict(
        self, 
        explicitTreeTracker: dict, 
        childrenIds: list[str]
        ) -> dict:
        """
        a recursive function, which converts the explicittreetracker into the recursive one.

        Parameters:
        explicitTreeTracker : dict
            the tree tracker of this class in explicit form
        childrenIds : list[str]
            the current children we observe

        Returns
        -------
        childrenDicts : dict
            the childrendicts, containing metadata

        """
        # initialize an empty dict, for the return
        childrenDicts = list()
        
        # go through all children
        for childId in childrenIds:
            childDict = dict()
            childDict["id"] = childId
            explicitChildDict: dict = explicitTreeTracker[childId]

            # copy all the attribute values of the treetracker
            for attribute in explicitChildDict:
                childDict[attribute] = explicitChildDict[attribute]

            isChildSplitter: bool = ("children" in explicitChildDict)

            # if encountering a splitter, do the method again
            if isChildSplitter:
                childDict["children"] = self._explicit_to_recursive_dict(
                    explicitTreeTracker, 
                    explicitChildDict["children"]
                )
            
            childrenDicts.append(childDict)

        return childrenDicts


    def _add_splitter(self, orientation: str, focusedWidget: NeoAnalyticsSingleton) -> None:
        """
        slices a focused widget into two new ones

        Parameters
        ----------
        orientation : str
            the orientation of the wanted slice
        focusedWidget : NeoAnalyticsSingleton
            the tile, which should get sliced 

        """
        if orientation == "horizontal":
            qtOrientation: Qt.Orientation = Qt.Orientation.Horizontal
        elif orientation == "vertical": 
            qtOrientation: Qt.Orientation = Qt.Orientation.Vertical

        parentSplitter: QSplitter = focusedWidget.parent()
        # check if the parent really is a splitter
        if not isinstance(parentSplitter, QSplitter):
            return

        qtParentOrientation: Qt.Orientation = parentSplitter.orientation()

        # HACK: this is proprietary and needs future change
        uniqueWidgetId: int = len(self.widgets)
        uniqueSplitId: int = len(self.splitter)
    
        newWidget: NeoAnalyticsSingleton = self._make_panel()
        # set id
        newWidgetId: str = f"Widget_{uniqueWidgetId}"
        newWidget.setProperty("id", newWidgetId)
        # get the position
        positionOfFocusedWidget: int = parentSplitter.indexOf(focusedWidget)
 
        # if the orientation matches, no splitter is created. instead just add a widget
        if qtOrientation == qtParentOrientation:
            # update treetracker
            self.treetracker[parentSplitter.property("id")]["children"].insert(positionOfFocusedWidget+1, newWidgetId)
            self.treetracker[newWidgetId] = dict()
            self.treetracker[newWidgetId]["parent"] = parentSplitter.property("id")
            print(self.treetracker)
            # set visible
            parentSplitter.insertWidget(positionOfFocusedWidget+1, newWidget)

            return

        # create the new splitter 
        newSplitterId: str = f"Splitter_{uniqueSplitId}"
        newSplitter: QSplitter = QSplitter(orientation=qtOrientation)
        newSplitter.setProperty("id", newSplitterId)
        self.splitter.append(newSplitter)

        # remove the widget and place the splitter accordingly 
        focusedWidget.setParent(None)
        self.treetracker[parentSplitter.property("id")]["children"].remove(focusedWidget.property("id"))
        parentSplitter.insertWidget(positionOfFocusedWidget, newSplitter)
        self.treetracker[parentSplitter.property("id")]["children"].insert(positionOfFocusedWidget, newSplitterId)

        # add the widgets to the new splitter and set correct sizes
        newSplitter.addWidget(focusedWidget)
        self.treetracker[focusedWidget.property("id")]["parent"] = newSplitterId
        newSplitter.addWidget(newWidget)
        self.treetracker[newWidgetId] = dict()
        self.treetracker[newWidgetId]["parent"] = newSplitterId
        newSplitter.setSizes([1, 1])
        parentSplitter.setSizes([1 for size in parentSplitter.sizes()])

        # adjust the treetracker
        self.treetracker[newSplitterId] = dict()
        self.treetracker[newSplitterId]["parent"] = parentSplitter.property("id")
        self.treetracker[newSplitterId]["children"] = [newWidgetId, focusedWidget.property("id")]
        print(self.treetracker)


class NeoAnalyticsSpaceWrapper(QWidget):
    """wrapper class for analyticsspaces
    
    Attributes
    ----------
    ui : Ui_Scroll_wrapper
        the raw Class, produced by compilation
    spaceinstance : NeoAnalyticsSpace
        An instance of the i3 like class

    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Scroll_wrapper()
        self.ui.setupUi(self)
        self.spaceInstance: NeoAnalyticsSpace = NeoAnalyticsSpace(self)
        # initializing a list of singletons, for proper management
        
        self.ui.scrollarea_insertlayout.addWidget(self.spaceInstance)

        self.ui.toolButton_dell.clicked.connect(self._delete_layout)
        self.ui.toolButton_loadl.clicked.connect(self._load_layout)
        self.ui.toolButton_savel.clicked.connect(self._save_layout)

    def _save_layout(self):

        self.spaceInstance._save_states()

    def _load_layout(self):
        pathToRecursiveTree: str = locPathSet_c + "ctr.json"
        recursiveTree: dict = readJsonFile(pathToRecursiveTree)

        self.spaceInstance.deleteLater()
        self.spaceInstance = NeoAnalyticsSpace(self, tree=recursiveTree)

        self.ui.scrollarea_insertlayout.addWidget(self.spaceInstance)

    def _delete_layout(self):

        self.spaceInstance.deleteLater()
        self.spaceInstance = NeoAnalyticsSpace(self)

        self.ui.scrollarea_insertlayout.addWidget(self.spaceInstance)

