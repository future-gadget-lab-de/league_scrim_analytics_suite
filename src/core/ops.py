

from src.core.match import loadMatchData
from src.database.wrapper import importData
from src.utils import transformPathtoFileList
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

    files = transformPathtoFileList(PathToFolder)

    for file in files:
        
        metadata, playerdata, blueteamdata, redteamdata = loadMatchData(file)
        importData([metadata], [blueteamdata, redteamdata], playerdata)


