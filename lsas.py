from src.match import loadMatchData
from src.utils import getMatchCount
import os, os.path


# Check how many Matchfiles exist
matchcount  = getMatchCount()



metadata, playerdata, blueteamdata, redteamdata, data_file = loadMatchData()

print(metadata, playerdata, blueteamdata, redteamdata, data_file)


