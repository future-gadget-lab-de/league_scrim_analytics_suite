"""this file serves as a entrypoint for operations, which are supported across .csv or mariadb option"""
from loguru import logger
from src.config import readSettings, settings_list_c
from src.database.csv.execution import insertDataAsCsv, readCsvs, runSelectOnDfs
from src.database.mariadb.execution import executeQuery, buildConnection, getCursorSelect
from src.database.queries import returnMatchfileQuery
from src.database.csv.manipulation import listOfDictsToDF
import pandas as pd

def importData(metadata: list[dict], teamdata: list[dict], playerdata: list[dict]) -> None:
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
                    
                insertDataAsCsv(metadata, teamdata, playerdata)
                
            case "1":
                
                queries = returnMatchfileQuery(metadata, teamdata, playerdata)

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

    match settings_lsas["mariadb"]:
        case "1":
            conn, cur = buildConnection()
            executeQuery([query], conn, cur)

            output = getCursorSelect(cur)
                        
            conn.close()
            cur.close()

            return listOfDictsToDF(output)

        case "0":
            dframes = readCsvs()

            table_dict = {
                "metadata": dframes[0],
                "teamdata": dframes[1],
                "playerdata": dframes[2]
            }

            if dframes[0].empty or dframes[1].empty or dframes[2].empty:
                return pd.DataFrame()

            return runSelectOnDfs(query, table_dict)
