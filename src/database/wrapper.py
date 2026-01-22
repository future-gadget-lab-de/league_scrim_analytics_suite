"""this file serves as a entrypoint for operations, which are supported across .csv or mariadb option"""
from loguru import logger
from src.core.structure import GameTable
from src.config import config, Configs
from src.database.csv.execution import insertDataAsCsv, runSelectOnDfs, readCsvData
from src.database.mariadb.execution import executeQuery, buildConnection, getCursorSelect
from src.database.queries import returnMatchfileQuery, returnSelectQuery
import pandas as pd

def importData(tabledict: dict[GameTable, pd.DataFrame]) -> None:
    """
    imports the three major datasets into the database

    Parameters
    ----------
    metadata : list[dict]
        the metadata of a provided game
    teamdata : list[dict]
        the red- and blueteamdata of a game
    playerdata : list[dict]
        the data of all 10 players of a game
    
    """

    match config.general_settings[Configs.MAIN]["mariadb"]:

            case "0":
                    
                insertDataAsCsv(tabledict)
                
            case "1":
                
                queries = returnMatchfileQuery(tabledict)

                # build connection
                conn, cur = buildConnection()
                # execute the queries
                for query in queries:
                    executeQuery(query, conn, cur)

                # close
                conn.commit()
                conn.close()
                cur.close()

def getListOfStoredData() -> list[str]:
    """method, which downstreams the gameids of imported files"""

    importlabel = config.general_settings[Configs.MAIN]["import_label"]
    query = returnSelectQuery(GameTable.META.value,[importlabel])
    data = executeSelectQuery(query)

    if data.empty:
        return []

    return [str(label) for label in data[importlabel].values.tolist()]

def executeSelectQuery(query: str) -> pd.DataFrame:
    """
    executes a sql query on the database

    Parameters
    ----------
    query : str
        the .sql query, which will be executed

    Returns
    -------
    table : pd.DataFrame
        the resulting dataframe
        
    """
    logger.info(f"executing the .sql query: {query}")

    match config.general_settings[Configs.MAIN]["mariadb"]:
        case "1":

            conn, cur = buildConnection()
            executeQuery(query, conn, cur)
            conn.commit()
            output = getCursorSelect(cur)
            conn.close()
            cur.close()

            return output

        case "0":
            dframeDict = readCsvData()

            for ttype in GameTable:
                if dframeDict[ttype].empty:
                    return pd.DataFrame()

            return runSelectOnDfs(query, dframeDict)
