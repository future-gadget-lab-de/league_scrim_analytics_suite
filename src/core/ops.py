import logging
logger = logging.getLogger(__name__)

import csv, os
from src.core.match import loadMatchData
from src.database.queries import returnInsertQuery
from src.database.execution import executeQuery, buildConnection
from src.database.sqltemplates.template import importSQLQueries
from src.utils import readSettingsFile, writeSettingsFile, addDictToCsv, list_relative_filepaths, getRelPath
from src.config import locPath_c


def importMatchfileData(PathToFolder: str) -> None:
    """
    imports a matchfile

    Parameters
    ----------
    PathToFolder : str
        the relative (or absolute) path to a matchfile or folder of matchfiles
    
    """

    relPathToFolder = PathToFolder
    if os.path.isabs(PathToFolder):
        relPathToFolder = getRelPath(PathToFolder)

    if os.path.isfile(relPathToFolder):
        files = [relPathToFolder]
    else: # if it is a directory
        files = list_relative_filepaths(relPathToFolder)

    settings_loc = readSettingsFile(locPath_c)
    settings = readSettingsFile(settings_loc["lsas"])

    for file in files:
        metadata, playerdata, blueteamdata, redteamdata = loadMatchData(file)

        match settings["mariadb"]:
            case "0":
                addDictToCsv(metadata, settings["csv_directory"]+"metadata.csv")
                for dict_ in playerdata:
                    addDictToCsv(dict_, settings["csv_directory"]+"playerdata.csv")
                addDictToCsv(blueteamdata, settings["csv_directory"]+"teamdata.csv")
                addDictToCsv(redteamdata, settings["csv_directory"]+"teamdata.csv")



                logger.info("Loading the matchfile in the location: %s", PathToFolder)
                
            case "1":
                queries = list()

                queries.append(returnInsertQuery("metadata",metadata))
                for playerdict in playerdata:
                    queries.append(returnInsertQuery("playerdata",playerdict))
                queries.append(returnInsertQuery("teamdata",blueteamdata))
                queries.append(returnInsertQuery("teamdata",redteamdata))

                logger.info("Loading the matchfile in the location: %s", PathToFolder)

                conn, cur = buildConnection()
                executeQuery(queries, conn, cur)

def clearData():
    """
    clears all Data out of the connected databases or the .csv directory
    """
    settings_loc = readSettingsFile(locPath_c)
    settings = readSettingsFile(settings_loc["lsas"])

    match settings["mariadb"]:
        case "0":
            os.remove(settings["csv_directory"]+"metadata.csv")
            os.remove(settings["csv_directory"]+"playerdata.csv")
            os.remove(settings["csv_directory"]+"teamdata.csv")

            logger.debug("Removing all .csv files")
            
        case "1":
            delete_queries = importSQLQueries("src/database/sqltemplates/db_delete_alldata.sql")

            logger.debug("Removing all contents of database tables.")

            conn, cur = buildConnection()
            executeQuery(delete_queries, conn, cur)

def databaseSetup():
    """
    Setups the connected database with the correct datatypes 
    """
    create_queries = importSQLQueries("src/database/sqltemplates/db_creation_dump.sql")

    logger.debug("Creating DB Format.")

    conn, cur = buildConnection()
    executeQuery(create_queries, conn, cur)

