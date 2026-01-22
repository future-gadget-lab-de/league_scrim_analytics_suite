import pandas as pd
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
    metadata : list[dict]
        the metadata of a provided game
    teamdata : list[dict]
        the red- and blueteamdata of a game
    playerdata : list[dict]
        the data of all 10 players of a game
    
    """

    match config.general_settings[Configs.MAIN]["mariadb"]:

        case "0":
                
            DataToCsv(tabledict)
            
        case "1":
            
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
