"""Contains methods, which are used for writing processed data into the persistant storage."""

import pandas as pd
from loguru import logger
from src.core.config import config, Configs
from src.core.meta import GameTable, TimeTable, ImportType
from src.core.io.csv import DataToCsv
from src.core.io.mariadb import buildConnection, executeQuery
from src.utils.sqlquery import returnInsertQuery

def writeData(tabledict: dict[GameTable, pd.DataFrame], typ: ImportType) -> None:
    """
    imports the three major datasets into the database

    Parameters
    ----------
    tabledict : dict[GameTable, pd.DataFrame]
        the main dataframe this program operates on
    
    """
    logger.trace("Start writing data to persistant storage.")
    match config.general_settings[Configs.PROF]["mode"]:

        case "csv":
            logger.trace("Writing in CSV mode.")
            DataToCsv(tabledict, typ)
            
        case "db":
            logger.trace("Writing in DB mode.")
            
            conn, cur = buildConnection()
            try:
                match typ:
                    case ImportType.GENERAL:
                        dub = "gameid"
                    case ImportType.TIMELINE:
                        dub = "matchid"
                    
                for tabletype in typ.value:
                    # build the query
                    query = returnInsertQuery(tabletype.value, tabledict[tabletype], ignoreDuplicateOn=dub)
                    # execute the query
                    executeQuery(query, conn, cur)

                conn.commit()
            finally:
                cur.close()
                conn.close()
