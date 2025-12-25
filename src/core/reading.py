import logging
logger = logging.getLogger(__name__)

import csv
from src.core.match import loadMatchData
from src.database.queries import returnInsertQuery
from src.database.execution import executeQuery, buildConnection
from src.utils import readSettingsFile, addDictToCsv

def importMatchfileData(relPathToFile: str) -> None:

    settings = readSettingsFile("config/lsas.conf")
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



