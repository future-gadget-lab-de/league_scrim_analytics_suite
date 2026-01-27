"""this file serves as a entrypoint for operations, which are supported across .csv or mariadb option"""
from loguru import logger
import pandas as pd
from src.core.meta import GameTable
from src.core.config import config, Configs
from src.core.io.csv import runSelectOnCsv, csvToData
from src.core.io.mariadb import executeQuery, buildConnection, getCursorSelect

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

    match config.general_settings[Configs.PROF]["mode"]:
        case "db":

            conn, cur = buildConnection()
            executeQuery(query, conn, cur)
            conn.commit()
            output = getCursorSelect(cur)
            conn.close()
            cur.close()

            return output

        case "csv":
            dframeDict = csvToData()

            for ttype in GameTable:
                print(dframeDict[ttype])
                if dframeDict[ttype].empty:

                    return pd.DataFrame()

            return runSelectOnCsv(query, dframeDict)
