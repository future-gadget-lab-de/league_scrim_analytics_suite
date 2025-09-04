from src.match import loadMatchData
from src.utils import getMatchCount, readDatabaseConfig
from src.database import insertMetadata
import os, os.path


# Check how many Matchfiles exist
matchcount  = getMatchCount()

db_conf = readDatabaseConfig()
insertMetadata(7493735947, '15.16', '2025-08-13', '0:33:35',db_conf)

#metadata, playerdata, blueteamdata, redteamdata, data_file = loadMatchData()

#print(metadata, playerdata, blueteamdata, redteamdata, data_file)


