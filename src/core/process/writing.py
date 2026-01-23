"""Contains methods, which are used for writing processed data into the persistant storage."""

import pandas as pd
from loguru import logger
from src.core.config import config, Configs
from src.core.meta import GameTable
from src.core.io.csv import DataToCsv
from src.core.io.mariadb import buildConnection, executeQuery
from src.utils.sqlquery import returnInsertQuery

def writeData(tabledict: dict[GameTable, pd.DataFrame]) -> None:
    """
    imports the three major datasets into the database

    Parameters
    ----------
    tabledict : dict[GameTable, pd.DataFrame]
        the main dataframe this program operates on
    
    """
    logger.trace("Start writing data to persistant storage.")
    match config.general_settings[Configs.MAIN]["mariadb"]:

        case "0":
            logger.trace("Writing in CSV mode.")
            DataToCsv(tabledict)
            
        case "1":
            logger.trace("Writing in DB mode.")
            
            conn, cur = buildConnection()
            try:
                for tabletype in GameTable:
                    # build the query
                    query = returnInsertQuery(tabletype.value, tabledict[tabletype], ignoreDuplicateOn="gameid")
                    # execute the query
                    executeQuery(query, conn, cur)
                conn.commit()
            finally:
                cur.close()
                conn.close()
