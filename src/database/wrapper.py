"""this file serves as a entrypoint for operations, which are supported across .csv or mariadb option"""
from loguru import logger
from src.core.structure import GameTable
from src.config import readSettings, settings_list_c
from src.database.csv.execution import insertDataAsCsv, runSelectOnDfs, readCsvData
from src.database.mariadb.execution import executeQuery, buildConnection, getCursorSelect
from src.database.queries import returnMatchfileQuery
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
    settings_lsas = readSettings(settings_list_c[0])

    match settings_lsas["mariadb"]:

            case "0":
                    
                insertDataAsCsv(tabledict)
                
            case "1":
                
                queries = returnMatchfileQuery(tabledict)

                # build connection
                conn, cur = buildConnection()
                # execute the queries
                executeQuery(queries, conn, cur)
                # close
                conn.close()
                cur.close()

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
    settings_lsas = readSettings(settings_list_c[0])

    logger.info(f"executing the .sql query: {query}")

    match settings_lsas["mariadb"]:
        case "1":

            conn, cur = buildConnection()
            executeQuery([query], conn, cur)

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
