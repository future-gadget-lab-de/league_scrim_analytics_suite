import pandas as pd
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
    
    """

    rawdict: dict = readJsonFile(relPathToFile)

    match config.general_settings[Configs.MAIN]["V5"]:

        case "1":
            exit(1) # unsupported right now
            tabledict: dict[GameTable, pd.DataFrame] = extractRawTables(rawdict, ImportPipeline.MATCHV5)

        case "0":
            tabledict: dict[GameTable, pd.DataFrame] = extractRawTables(rawdict, ImportPipeline.CLIENT)
            translateTables(tabledict, ImportPipeline.CLIENT)

    return tabledict


def listImportedMatchfiles() -> list[str]:
    """method, which downstreams the gameids of imported files"""

    importlabel = config.general_settings[Configs.MAIN]["import_label"]
    query = returnSelectQuery(GameTable.META.value,[importlabel])
    data = executeSelectQuery(query)

    if data.empty:
        return []

    return [str(label) for label in data[importlabel].values.tolist()]