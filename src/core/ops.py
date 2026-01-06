import logging
logger = logging.getLogger(__name__)

import csv, os
from src.core.match import loadMatchData
from src.database.queries import returnInsertQuery
from src.database.execution import executeQuery, buildConnection, getCursorSelect
from src.database.sqltemplates.template import importSQLQueries
from src.utils import readSettingsFile, writeSettingsFile, addDictToCsv, transformPathtoFileList
from src.config import locPath_c


def importMatchfileData(PathToFolder: str) -> None:
    """
    imports a matchfile

    Parameters
    ----------
    PathToFolder : str
        the relative (or absolute) path to a matchfile or folder of matchfiles
    
    """

    files = transformPathtoFileList(PathToFolder)

    settings_loc = readSettingsFile(locPath_c)
    settings = readSettingsFile(settings_loc["lsas"])

    for file in files:

        match settings["old_patch_support"]:
            case "1":
                metadata, playerdata, blueteamdata, redteamdata = loadMatchData(file, True)
            case "0":
                metadata, playerdata, blueteamdata, redteamdata = loadMatchData(file)

        match settings["mariadb"]:
            case "0":

                addDictToCsv(metadata, settings["csv_directory"]+"/metadata.csv")
                for dict_ in playerdata:
                    addDictToCsv(dict_, settings["csv_directory"]+"/playerdata.csv")
                addDictToCsv(blueteamdata, settings["csv_directory"]+"/teamdata.csv")
                addDictToCsv(redteamdata, settings["csv_directory"]+"/teamdata.csv")

                logger.info("Loading the matchfile in the location: %s", PathToFolder)
                
            case "1":
                
                match settings_loc["connected"]:
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
                        conn.close()
                        cur.close()
                    case "0":
                        raise Exception("Your MariaDB Config can't establish a connection. Reconfigure the database.conf!")
                        sys.exit(1)

def clearData() -> None:
    """
    clears all Data out of the connected databases or the .csv directory
    """
    settings_loc = readSettingsFile(locPath_c)
    settings = readSettingsFile(settings_loc["lsas"])

    match settings["mariadb"]:
        case "0":
            os.remove(settings["csv_directory"]+"/metadata.csv")
            os.remove(settings["csv_directory"]+"/playerdata.csv")
            os.remove(settings["csv_directory"]+"/teamdata.csv")

            logger.debug("Removing all .csv files")
            
        case "1":
            delete_queries = importSQLQueries("src/database/sqltemplates/db_delete_alldata.sql")

            logger.debug("Removing all contents of database tables.")

            conn, cur = buildConnection()
            executeQuery(delete_queries, conn, cur)
            conn.close()
            cur.close()

def databaseSetup() -> None:
    """
    Setups the connected database with the correct datatypes 
    """
    create_queries = importSQLQueries("src/database/sqltemplates/db_creation_dump.sql")

    logger.debug("Creating DB Format.")

    conn, cur = buildConnection()
    executeQuery(create_queries, conn, cur)
    conn.close()
    cur.close()

def executeSQLFiles(pathToFile: str) -> None | list[dict]:
    """
    executes a .sql file. if only one file is given and the last command is a SELECT, it also outputs a dict

    Parameters
    ----------
    PathToFolder : str
        the relative (or absolute) path to a .sql file

    Returns
    -------
    possible_select : list[dict]
        can return a dict, if one file is passed, with select at last

    """

    settings_loc = readSettingsFile(locPath_c)
    
    files = transformPathtoFileList(pathToFile)

    queries_of_file = list[list[str]]()

    for file in files:
        queries_of_file.append(importSQLQueries(file))

    match settings_loc["connected"]:
        case "1":

            conn, cur = buildConnection()
            
            for queries in queries_of_file:
                print(queries)
                executeQuery(queries, conn, cur)

            print(queries_of_file)
            if len(files) == 1 and queries_of_file[0][-1].startswith("SELECT"):
                output = getCursorSelect(cur)
                
                conn.close()
                cur.close()

                return output

            conn.close()
            cur.close()
            return None

        case "0":
            raise Exception("Your MariaDB Config can't establish a connection. Reconfigure the database.conf!")
            sys.exit(1)

