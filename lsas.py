from src.utils import loadDatabaseConfig, moveFile, list_relative_filepaths
from src.database.queries import returnInsertQuery, returnMatchfileQuery
from src.database.execution import executeQuery, buildConnection
from src.database.sqltemplates.template import importSQLQueries
from src.visuals.simplefrontend import SimpleFrontend
from PySide6.QtWidgets import QApplication
import os, os.path, sys, datetime

def databaseSetup():
    # Check how many Matchfiles exist
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    db_conf = loadDatabaseConfig()
    delete_queries = importSQLQueries("src/database/sqltemplates/db_delete_alldata.sql")
    create_queries = importSQLQueries("src/database/sqltemplates/db_creation_dump.sql")

    matchfiles = list_relative_filepaths("gamefiles/matchdata")

    matchfile_queries = dict()
    for match in matchfiles:
        matchfile_queries[match] = returnMatchfileQuery("gamefiles/matchdata/"+match)

    conn, cur = buildConnection(db_conf)
    
    try:
        executeQuery(delete_queries, conn, cur)
        executeQuery(matchfile_queries[matchfiles[0]], conn, cur)

    finally: 
        cur.close()

def runFrontend() -> None:
    app = QApplication(sys.argv)
    # basically will "starten" execute the passed function
    window = SimpleFrontend(databaseSetup)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    databaseSetup()
    #runFrontend()

