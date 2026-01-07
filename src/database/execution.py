import logging
logger = logging.getLogger(__name__)

import mariadb, sys

from src.utils import readSettingsFile
from src.config import locPath_c
#TODO: Rewrite Logging
def buildConnection() -> tuple:
    """builds a connection to mariadb server

    Uses connection parameters to build a connection and a cursor(interface with server) to a database host

    Returns
    -------
    conn : connection
        Handles the connection to a MariaDB or MySQL database server. It encapsulates a database session. 
    cur : cursor
        Executes SQL statements and procedures, and manages fetching results.
    """
    settings_loc = readSettingsFile(locPath_c)
    conn_params = readSettingsFile(settings_loc["database"])
    conn_params['port'] = int(conn_params['port']) 
    conn = mariadb.connect(**conn_params)
    logger.info("Connection to MariaDB Server established.")
    cur = conn.cursor()
    return conn, cur

def executeQuery(queries: list[str], conn, cur):
    """executes a list of queries.

    This method takes a conn, cur from a established mariadb connection and executes a list of passed queries.

    Parameters
    ----------
    queries : list[str]
        a list of sql queries
    conn : connection
        connection to a mariadb server instance
    cur : cursor
        cursor of a mariadb server instance
    """
    for query in queries:
        try:
            logger.debug("will execute the sql query: %s", query)
            cur.execute(query)
            if len(query) > 100:
                logger.info("Executed a sql query. For Detail, adjust loglevel to DEBUG.")
            else:
                logger.info("Executed the sql query: %s", query)
            conn.commit()
            #TODO: Log query here.
        except mariadb.Error as e:
            cur.close()
            logger.error("Error connecting to MariaDB Platform: %s", e)
            sys.exit(1)
    
