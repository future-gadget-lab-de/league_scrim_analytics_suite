from src.match import loadMatchData
from src.utils import getMatchCount, loadDatabaseConfig, moveFileDone
from src.database import insertData
from src.frontend.simplefrontend import SimpleFrontend
from PySide6.QtWidgets import QApplication
import os, os.path, sys

def databaseSetup():
    # Check how many Matchfiles exist
    matchcount  = getMatchCount()
    db_conf = loadDatabaseConfig()

    for i in range (0, matchcount):
        metadata, playerdata, blueteamdata, redteamdata, data_file = loadMatchData()
        gameid = metadata[0]
        
        # insertion of metadata
        insertData(metadata, db_conf, gameid, "metadata")

        # insertion of teamdata
        insertData(blueteamdata, db_conf, gameid, "teamdata")
        insertData(redteamdata, db_conf, gameid, "teamdata")

        # insertion of playerdata
        for i in range(0,10):
            insertData(playerdata[i], db_conf, gameid, "playerdata")
        print("INFO: Inserted Game: " + str(gameid))

        # removing successful imported files
        moveFileDone(data_file, gameid)
        print("INFO: Moved Gamefile: " + str(gameid))

def runFrontend() -> None:
    app = QApplication(sys.argv)
    window = SimpleFrontend(databaseSetup)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    runFrontend()

