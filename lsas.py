from log_config import setup_logging
import logging
logger = logging.getLogger(__name__)

import os, os.path, sys
# gui stuff
from src.visuals.simplefrontend import SimpleFrontend
from src.visuals.windows.main_window import MainWindow
from PySide6.QtWidgets import QApplication
# mariadb stuff
from src.database.queries import returnInsertQuery, returnMatchfileQuery
from src.database.execution import executeQuery, buildConnection
from src.database.sqltemplates.template import importSQLQueries

from src.utils import list_relative_filepaths

def databaseSetup():
    # Check how many Matchfiles exist
    delete_queries = importSQLQueries("src/database/sqltemplates/db_delete_alldata.sql")
    create_queries = importSQLQueries("src/database/sqltemplates/db_creation_dump.sql")

    matchfiles = list_relative_filepaths("gamefiles/matchdata")

    matchfile_queries = dict()
    for match in matchfiles:
        matchfile_queries[match] = returnMatchfileQuery("gamefiles/matchdata/"+match)

    conn, cur = buildConnection()
    
    try:
        executeQuery(delete_queries, conn, cur)
        executeQuery(matchfile_queries[matchfiles[0]], conn, cur)

    finally: 
        logger.info("Connection to MariaDB Server closed")
        cur.close()

def runFrontend() -> None:
    app = QApplication(sys.argv)
    # basically will "starten" execute the passed function
    window = SimpleFrontend(databaseSetup)
    window.show()
    sys.exit(app.exec())

def runAdvancedFrontend() -> None:
    app = QApplication(sys.argv)
    # basically will "starten" execute the passed function
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    setup_logging(level = "INFO")
    runAdvancedFrontend()
    #databaseSetup()
    #runFrontend()

