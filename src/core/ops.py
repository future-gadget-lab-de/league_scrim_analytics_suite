
from src.core.extracting.client import loadDumpMatchData
from src.core.extracting.apiV5 import loadV5MatchData
from src.database.wrapper import importData
from src.utils import transformPathtoFileList
from src.config import readSettings, settings_list_c
from loguru import logger

#TODO: Rewrite Logging
def importMatchfileData(PathToFolder: str) -> None:
    """
    imports a matchfile

    Parameters
    ----------
    PathToFolder : str
        the relative (or absolute) path to a matchfile or folder of matchfiles
    
    """
    settings_lsas = readSettings(settings_list_c[0])

    files = transformPathtoFileList(PathToFolder)

    for file in files:

        if settings_lsas["V5"] == "1":
            metadata, playerdata, blueteamdata, redteamdata = loadV5MatchData(file)

        else:
            metadata, playerdata, blueteamdata, redteamdata = loadDumpMatchData(file)

        if len(metadata) == 0:
            continue

        importData([metadata], [blueteamdata, redteamdata], playerdata)
