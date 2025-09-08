from src.match import loadMatchData
from src.utils import getMatchCount, readDatabaseConfig, moveFileDone
from src.database import insertData
import os, os.path
S



# Check how many Matchfiles exist
matchcount  = getMatchCount()
db_conf = readDatabaseConfig()
for i in range (0, matchcount):
    metadata, playerdata, blueteamdata, redteamdata, data_file = loadMatchData()
    gameid = metadata[0]
    #Insertions
    insertData(metadata, db_conf, gameid, "metadata")
    insertData(blueteamdata, db_conf, gameid, "teamdata")
    insertData(redteamdata, db_conf, gameid, "teamdata")
    for i in range(0,10):
        insertData(playerdata[i], db_conf, gameid, "playerdata")
    print("INFO: Inserted Game: " + str(gameid))
    moveFileDone(data_file, gameid)
    print("INFO: Moved Gamefile: " + str(gameid))
    



#metadata, playerdata, blueteamdata, redteamdata, data_file = loadMatchData()

#print(metadata, playerdata, blueteamdata, redteamdata, data_file)


