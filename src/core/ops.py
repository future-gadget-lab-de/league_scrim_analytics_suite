

from src.core.match import loadDumpMatchData
from src.core.apimatch import loadV5MatchData
from src.database.wrapper import importData
from src.utils import transformPathtoFileList
from loguru import logger

#TODO: Rewrite Logging
def importMatchfileData(PathToFolder: str, V5: bool = False) -> None:
    """
    imports a matchfile

    Parameters
    ----------
    PathToFolder : str
        the relative (or absolute) path to a matchfile or folder of matchfiles
    
    """

    files = transformPathtoFileList(PathToFolder)

    for file in files:

        if V5:
            metadata, playerdata, blueteamdata, redteamdata = loadV5MatchData(file)

        else:
            metadata, playerdata, blueteamdata, redteamdata = loadDumpMatchData(file)

        importData([metadata], [blueteamdata, redteamdata], playerdata)
