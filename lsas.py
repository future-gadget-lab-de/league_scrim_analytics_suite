from src.utils import loadDatabaseConfig, moveFile, list_relative_filepaths
from src.database.queries import returnInsertQuery, returnMatchfileQuery
from src.database.execution import executeQuery
from src.database.sqltemplates.template import importSQLQueries
from src.visuals.simplefrontend import SimpleFrontend
from PySide6.QtWidgets import QApplication
import os, os.path, sys

def databaseSetup():
    # Check how many Matchfiles exist
    db_conf = loadDatabaseConfig()
    delete_queries = importSQLQueries("src/database/sqltemplates/db_delete_alldata.sql")
    create_queries = importSQLQueries("src/database/sqltemplates/db_creation_dump.sql")

    matchfiles = list_relative_filepaths("gamefiles/matchdata")

    print(matchfiles)

    matchfile_queries = dict()

    for match in matchfiles:
        matchfile_queries[match] = returnMatchfileQuery("gamefiles/matchdata/"+match)
    
    QUERIES = delete_queries
    QUERIES = matchfile_queries[matchfiles[1]]

    #print(QUERIES)

    for query in QUERIES:
        print(query)
        executeQuery(query, db_conf)

def runFrontend() -> None:
    app = QApplication(sys.argv)
    # basically will "starten" execute the passed function
    window = SimpleFrontend(databaseSetup)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    databaseSetup()
    #runFrontend()

