from src.match import loadMatchData
from src.utils import getMatchCount, readDatabaseConfig
from src.database import insertMetadata, insertTeamdata
import os, os.path


# Check how many Matchfiles exist
matchcount  = getMatchCount()

db_conf = readDatabaseConfig()
metadata, playerdata, blueteamdata, redteamdata, data_file = loadMatchData()
gameid = metadata[0]
#insertMetadata(metadata,        db_conf,    gameid)
insertTeamdata(blueteamdata,    db_conf,    gameid)
insertTeamdata(redteamdata,     db_conf,    gameid)
#for i in range (0,10):
#    insertTeamdata(playerdata[i], db_conf)


#metadata, playerdata, blueteamdata, redteamdata, data_file = loadMatchData()

#print(metadata, playerdata, blueteamdata, redteamdata, data_file)


