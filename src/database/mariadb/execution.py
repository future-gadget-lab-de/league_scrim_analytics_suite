"""
This file contains code, which either
- builds a connection to a mariadb server or
- or executes sql queries on a mariadb server
"""

import mariadb, sys
from src.config import writeInternalSettings, readInternalSettings, readSettings, writeSettings, settings_list_c
from src.utils import transformPathtoFileList
from src.database.mariadb.sqltemplates.template import importSQLQueries
from loguru import logger

def updateConnectionState() -> str:
    """
    updates the the connection status of lsas and writes it into the config files.

    Returns
    -------
    connection_status : str
        either a '1' for connected or a '0' for disconnected
    
    """
    settings_int = readInternalSettings()
    settings_lsas = readSettings(settings_list_c[0])

    try:
        buildConnection()
        settings_int["_connected"] = "1"

        writeInternalSettings(settings_int)
    except:
        settings_int["_connected"] = "0"
        settings_lsas["mariadb"] = "0"

        writeSettings(settings_list_c[0], settings_lsas)
        writeInternalSettings(settings_int)
    
    return settings_int["_connected"]

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

    conn_params: dict[str] = readSettings(settings_list_c[1])
    conn_params['port'] = int(conn_params['port']) 

    conn = mariadb.connect(**conn_params)
    logger.debug("Connection to MariaDB Server established.")
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
            logger.debug(f"will execute the sql query: {query}", )
            cur.execute(query)
            if len(query) > 100:
                logger.info("Executed a sql query. For Detail, adjust loglevel to DEBUG.")
            else:
                logger.info(f"Executed the sql query: {query}")
            conn.commit()
            #TODO: Log query here.
        except mariadb.Error as e:
            cur.close()
            logger.error(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
    
def executeSQLFiles(pathToFile: str) -> None:
    """
    executes a .sql file. if only one file is given and the last command is a SELECT, it also outputs a dict

    Parameters
    ----------
    PathToFolder : str
        the relative (or absolute) path to a .sql file

    """

    settings_lsas = readSettings(settings_list_c[0])
    
    files = transformPathtoFileList(pathToFile)

    queries_of_file = list[list[str]]()

    for file in files:
        queries_of_file.append(importSQLQueries(file))

    match settings_lsas["mariadb"]:
        case "1":

            conn, cur = buildConnection()
            
            for queries in queries_of_file:
                executeQuery(queries, conn, cur)

            conn.close()
            cur.close()

        case "0":
            raise Exception("Your MariaDB Config can't establish a connection. Reconfigure the your settings.")
            sys.exit(1)

def databaseSetup() -> None:
    """
    Setups the connected database with the correct datatypes 
    """
    create_queries = importSQLQueries("src/database/mariadb/sqltemplates/db_creation_dump.sql")

    logger.debug("Creating DB Format.")

    conn, cur = buildConnection()
    executeQuery(create_queries, conn, cur)
    conn.close()
    cur.close()

def getCursorSelect(cur) -> list[dict]:
    """returns the content of the cursor, after a done SELECT query.
    
    Parameters
    ----------
    cur
        the cursor of the described mariadb connection after a SELECT
        
    Returns
    -------
    parsed_rows : list[dict]
        the parsed rows in a raw data format
        
    """
    cols = [d[0] for d in cur.description]
    parsed_rows = list[dict]()

    for row in cur:
        parsed_rows.append(dict(zip(cols, row)))
    return parsed_rows


