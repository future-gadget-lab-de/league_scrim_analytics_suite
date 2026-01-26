"""contains methods for reading data, that will be processed"""
import pandas as pd
import numpy as np
from loguru import logger
from src.core.config import config, Configs
from src.core.meta import GameTable
from src.core.process.extract import extractRawTables, ImportPipeline
from src.core.process.pipelines.client import translateTablesForClient
from src.core.io.wrapper import executeSelectQuery
from src.utils.io import readJsonFile
from src.utils.sqlquery import returnSelectQuery
from src.core.process.manager import centralmanager

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
    match config.general_settings[Configs.PROF]["format"]:

        case "matchv5":
            tabledict: dict[GameTable, pd.DataFrame] = extractRawTables(rawdict, ImportPipeline.MATCHV5)
            #translateTables(tabledict, ImportPipeline.MATCHV5)

        case "client":
            tabledict: dict[GameTable, pd.DataFrame] = extractRawTables(rawdict, ImportPipeline.CLIENT)
            logger.trace("constructed the dict: "+str(tabledict))

    logger.trace("Finished the import process for the file.")
    return tabledict


def translateCentralData(tables: dict[GameTable, pd.DataFrame]):




    for tabletype in GameTable:


        cols = centralmanager.recent_tables[tabletype].columns
        missing = [v for v in cols if v not in tables[tabletype].columns]

        tables[tabletype][missing] = 0

        tables[tabletype] = tables[tabletype][cols]

        tables[tabletype] = tables[tabletype].rename(centralmanager.namemap[tabletype], axis="columns")

        tables[tabletype] = tables[tabletype].reindex(sorted(tables[tabletype].columns), axis=1)
        
        tables[tabletype] = tables[tabletype].fillna(0)

        if not centralmanager.present[tabletype]:
            continue

        ifilter = centralmanager.filter[tabletype]

        tables[tabletype] = tables[tabletype].iloc[:,ifilter]

    



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