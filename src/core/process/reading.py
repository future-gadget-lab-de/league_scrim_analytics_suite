"""contains methods for reading data, that will be processed"""
import pandas as pd
from loguru import logger
from src.core.config import config, Configs
from src.core.meta import GameTable
from src.core.process.extract import extractRawTables, translateTables, ImportPipeline
from src.core.io.wrapper import executeSelectQuery
from src.utils.io import readJsonFile
from src.utils.sqlquery import returnSelectQuery

def importMatchfiles(relPathToFile: str) -> dict[GameTable, pd.DataFrame]:
    """
    imports a matchfile

    Parameters
    ----------
    relPathToFile : str
        the relative path to a matchfile
    
    Returns
    -------
    tabledict : dict[GameTable, pd.DataFrame]
        the table this program operates on
    """

    rawdict: dict = readJsonFile(relPathToFile)
    logger.trace(f"Start importing a matchfile in {relPathToFile}.")
    match config.general_settings[Configs.MAIN]["V5"]:

        case "1":
            exit(1) # unsupported right now
            tabledict: dict[GameTable, pd.DataFrame] = extractRawTables(rawdict, ImportPipeline.MATCHV5)

        case "0":
            tabledict: dict[GameTable, pd.DataFrame] = extractRawTables(rawdict, ImportPipeline.CLIENT)
            for tabletype in GameTable:
                tabledict[tabletype].to_csv(tabletype.value + ".csv")
            logger.trace("constructed the dict: "+str(tabledict))
            translateTables(tabledict, ImportPipeline.CLIENT)
    logger.trace("Finished the import process for the file.")
    return tabledict


def listImportedMatchfiles() -> list[str]:
    """method, which downstreams the gameids of imported files
    
    Returns
    -------
    games : list[str]
        a list of all games imported
        
    """

    importlabel = config.general_settings[Configs.MAIN]["import_label"]
    query = returnSelectQuery(GameTable.META.value,[importlabel])
    data = executeSelectQuery(query)

    if data.empty:
        return []

    return [str(label) for label in data[importlabel].values.tolist()]