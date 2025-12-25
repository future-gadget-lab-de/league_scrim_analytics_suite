from log_config import setup_logging
import logging
logger = logging.getLogger(__name__)

import os, os.path, sys
# gui stuff
from src.visuals.windows.main_window import MainWindow
from PySide6.QtWidgets import QApplication
# mariadb stuff
from src.database.queries import returnInsertQuery, returnMatchfileQuery
from src.database.execution import executeQuery, buildConnection
from src.database.sqltemplates.template import importSQLQueries

from src.utils import list_relative_filepaths

def runAdvancedFrontend() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    setup_logging(level = "DEBUG")
    runAdvancedFrontend()

