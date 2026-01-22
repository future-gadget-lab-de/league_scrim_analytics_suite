
from src.core.extracting.process import ImportPipeline, extractRawTables, translateTables
from src.database.wrapper import importData
from src.utils import transformPathtoFileList, loadjsonfiles
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

        rawdict: dict = loadjsonfiles(file)

        match settings_lsas["V5"]:

            case "1":
                exit(1) # unsupported right now
                tabledict: dict[GameTable, pd.DataFrame] = extractRawTables(rawdict, ImportPipeline.MATCHV5)

            case "0":
                tabledict: dict[GameTable, pd.DataFrame] = extractRawTables(rawdict, ImportPipeline.CLIENT)
                translateTables(tabledict, ImportPipeline.CLIENT)

        importData(tabledict)
