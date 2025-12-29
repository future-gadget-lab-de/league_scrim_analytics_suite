import logging
logger = logging.getLogger(__name__)

import csv, os
from src.core.match import loadMatchData
from src.database.queries import returnInsertQuery
from src.database.execution import executeQuery, buildConnection
from src.database.sqltemplates.template import importSQLQueries
from src.utils import readSettingsFile, writeSettingsFile, addDictToCsv

def enrollSettings(relPathToConf: str) -> None:
    """
    Enrolls settings files for the user

    relPathToConf : str
        the relative path to the config folder
    
    """

    settings_dict = {
        "lsas": {
            "config_directory": relPathToConf, 
            "csv_directory": "",
            "mariadb": "",
            "API_key": ""
        },
        "database" : {
            "host": "",
            "user": "",
            "password": "",
            "port": "",
            "database": ""
        }
    }

    for key in settings_dict.keys():
        relPathToFile = relPathToConf + "/" + str(key) + ".conf"

        try: 
            settings = readSettingsFile(relPathToConf + "/" + str(key) + ".conf")
        except: 
            settings = settings_dict[key]

        writeSettingsFile(settings, relPathToFile)
    

def importMatchfileData(relPathToFile: str) -> None:
    """
    imports a matchfile

    Parameters
    ----------
    relPathToFile : str
        the relative path to the matchfile
    
    """
    settings = readSettingsFile(".config/lsas.conf")
    metadata, playerdata, blueteamdata, redteamdata, data_file = loadMatchData(relPathToFile)

    match settings["mariadb"]:
        case "0":
            addDictToCsv(metadata, settings["csv_directory"]+"metadata.csv")
            for dict_ in playerdata:
                addDictToCsv(dict_, settings["csv_directory"]+"playerdata.csv")
            addDictToCsv(blueteamdata, settings["csv_directory"]+"teamdata.csv")
            addDictToCsv(redteamdata, settings["csv_directory"]+"teamdata.csv")

            logger.debug("Loading the matchfile in the location: %s", relPathToFile)
            
        case "1":
            queries = list()

            queries.append(returnInsertQuery("metadata",metadata))
            for playerdict in playerdata:
                queries.append(returnInsertQuery("playerdata",playerdict))
            queries.append(returnInsertQuery("teamdata",blueteamdata))
            queries.append(returnInsertQuery("teamdata",redteamdata))

            logger.debug("Loading the matchfile in the location: %s", relPathToFile)

            conn, cur = buildConnection()
            executeQuery(queries, conn, cur)

def clearData():
    """
    clears all Data out of the connected databases or the .csv directory
    """
    settings = readSettingsFile(".config/lsas.conf")

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

