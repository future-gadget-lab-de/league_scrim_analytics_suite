"""the wrapper class for a single instance of plot spaces"""
from __future__ import annotations

from loguru import logger

from src.core.config import locPathSet_c, config, Configs
from src.core.io.wrapper import executeSelectQuery
from src.core.analyse.plugin import ApplyTemplate, getPossiblePlots, executePlugin

from src.visuals.ui.generated.ui_NeoDiagrams import Ui_NeoDiagrams

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget


class NeoDiagrams(QWidget):
    """a class wrapper for the Diagrams tile, where an sql query or template file
    produces a figure

    Attributes
    ----------
    id : str
        this attribute is used internally to uniquely map a picture,
        to his corresponding widget
    
    ui : Ui_NeoDiagrams
        the class produced by compiling the corresponding ui file.
    
    """
    def __init__(self, ids: str, parent=None) -> None:
        super().__init__(parent)

        # attributes
        self.id: str = ids
        self.ui: Ui_NeoDiagrams = Ui_NeoDiagrams()
        self.ui.setupUi(self)

        # initial setup
        self._init_windows()

        # connects for functionality
        self.ui.checkBox_json.stateChanged.connect(self._update_states)
        self.ui.checkBox_sql.stateChanged.connect(self._update_states)
        self.ui.commandLink_plot.pressed.connect(self._execute_plot)
        self.ui.toolButton_sql.pressed.connect(self._show_dropdown)


    def _init_windows(self):
        """initializes all widgets in this class with a specific state.
        
        Here all widgets are disabled, since the user has to choose one of
        the provided methods of plotting in the first place.
        """
        # the initial state of all fields is that they are deactivated
        self.ui.commandLink_plot.setDisabled(True)
        self.ui.toolButton_sql.setDisabled(True)
        self.ui.comboBox_sql.setDisabled(True)
        self.ui.lineEdit_sql.setDisabled(True)
        self.ui.lineEdit_json.setDisabled(True)

    def _show_dropdown(self):
        """
        if the sql method is used, this method will spawn entries
        in the combobox, which are exactly the plugins, which apply on the given
        sql query.
        """
        query = self.ui.lineEdit_sql.text()
        possiblePlugins = getPossiblePlots([query])

        for plugins in possiblePlugins:
            plugname = list(plugins[0].keys())[-1]
            self.ui.comboBox_sql.addItems([plugname])

        self._update_states()


    def _update_states(self):
        """updates the state of all widgets according to checkboxstates"""

        jsonChecked = self.ui.checkBox_json.isChecked()
        self.ui.lineEdit_json.setDisabled(not jsonChecked)

        if not jsonChecked:
            self.ui.lineEdit_json.setText("")

        sqlChecked = self.ui.checkBox_sql.isChecked()
        self.ui.lineEdit_sql.setDisabled(not sqlChecked)
        self.ui.toolButton_sql.setDisabled(not sqlChecked)

        if not sqlChecked:
            self.ui.lineEdit_sql.setText("")
            self.ui.comboBox_sql.clear()

        isComboboxSet = self.ui.comboBox_sql.currentText() != ""
        self.ui.comboBox_sql.setDisabled(not isComboboxSet)

        applyabel = (jsonChecked != sqlChecked)
        self.ui.commandLink_plot.setDisabled(not applyabel)

    def _execute_plot(self):
        """executes plotting via the plugin module according to the given data"""

        sqlChecked = self.ui.checkBox_sql.isChecked()
        isComboboxSet = self.ui.comboBox_sql.currentText() != ""
        jsonChecked = self.ui.checkBox_json.isChecked()

        picpath = config.general_settings[Configs.MAIN]["metadata_directory"] \
                    + "/" + config.general_settings[Configs.MAIN]["current_prof"] \
                    + self.id + ".png"

        height = self.ui.picture_root.geometry().height()
        width = self.ui.picture_root.geometry().width()

        if isComboboxSet:
            DF = executeSelectQuery(self.ui.lineEdit_sql.text())
            executePlugin([DF], self.ui.comboBox_sql.currentText(), picpath, (width, height))
            self.ui.picture_root.setPixmap(QPixmap(picpath))

        if jsonChecked:
            ApplyTemplate(self.ui.lineEdit_json.text(), picpath, (width, height))
            self.ui.picture_root.setPixmap(QPixmap(picpath))

