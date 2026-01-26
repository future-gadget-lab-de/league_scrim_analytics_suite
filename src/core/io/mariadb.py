"""
This file contains code, which either
- builds a connection to a mariadb server or
- or executes sql queries on a mariadb server
"""

import mariadb, sys
import pandas as pd
from src.core.config import config, Configs
from src.utils.io import readSQLFile
from src.core.process.manager import centralmanager
from src.core.meta import GameTable
from loguru import logger

def updateConnectionState(customConf: dict | None = None) -> None:
    """
    updates the the connection status of lsas and writes it into the config files.

    Returns
    -------
    connection_status : str
        either a '1' for connected or a '0' for disconnected
    
    """


    logger.trace("Checking the Connectionstate.")
    try:
        buildConnection(customConf)
        config.volatile_settings["_connected"] = "1"
        config.writeSettings()
        logger.debug("successfully established a connection to mariadb.")
    except:
        config.volatile_settings["_connected"] = "0"
        config.writeSettings()
        logger.debug("connection failed.")

    

#TODO: Rewrite Logging
def buildConnection(customConf: dict | None = None) -> tuple:
    """builds a connection to mariadb server

    Uses connection parameters to build a connection and a cursor(interface with server) to a database host

    Returns
    -------
    conn : connection
        Handles the connection to a MariaDB or MySQL database server. It encapsulates a database session. 
    cur : cursor
        Executes SQL statements and procedures, and manages fetching results.
    """

    conn_params: dict[str, str] = config.general_settings[Configs.DB].copy()

    if customConf is not None:
        conn_params = customConf.copy()
    conn_params['port'] = int(conn_params['port']) 

    conn = mariadb.connect(**conn_params)
    logger.debug("Connection to MariaDB Server established.")
    cur = conn.cursor()
    return conn, cur

def executeQuery(query: str, conn, cur):
    """executes a list of queries.

    This method takes a conn, cur from a established mariadb connection and executes a list of passed queries.

    Parameters
    ----------
    query : str
        a sql query
    conn : connection
        connection to a mariadb server instance
    cur : cursor
        cursor of a mariadb server instance
    """
    try:
        logger.debug(f"will execute the sql query: {query}", )
        cur.execute(query)
        if len(query) > 100:
            logger.info("Executed a sql query. For Detail, adjust loglevel to DEBUG.")
        else:
            logger.info(f"Executed the sql query: {query}")
        #TODO: Log query here.
    except mariadb.Error as e:
        cur.close()
        logger.error(f"Error connecting to MariaDB Platform: {e}")
    
def executeSQLFile(pathToFile: str) -> None:
    """
    executes a .sql file. if only one file is given and the last command is a SELECT, it also outputs a dict

    Parameters
    ----------
    PathToFile: str
        the relative path to a .sql file

    """
    logger.trace(f"start executing the sql file: {pathToFile}.")
    match config.general_settings[Configs.PROF]["mode"]:
        
        case "db":
            conn, cur = buildConnection()
            queries = readSQLFile(pathToFile)

            for query in queries:
                executeQuery(query, conn, cur)

            conn.commit()
            conn.close()
            cur.close()

        case "csv":
            raise Exception("Your MariaDB Config can't establish a connection. Reconfigure the your settings.")
            sys.exit(1)

def databaseSetup() -> None:
    """
    Setups the connected database with the correct datatypes 
    """
    match config.general_settings[Configs.PROF]["mode"]:
        case "db":
            try:
                # create_queries = importSQLQueries("src/core/io/sqlfiles/db_creation_dump.sql")
                create_queries = getCreationQueries()
                logger.debug("Creating DB Format.")

                conn, cur = buildConnection()
                for query in create_queries:
                    executeQuery(query, conn, cur)
                
                conn.commit()
                conn.close()
                cur.close()
            except:
                logger.debug("Database structure already initialized")
        case "csv":
            logger.debug("CSV Mode, therefore no structure creation.")

def getCreationQueries():
    
    tables = centralmanager.recent_tables

    queries = [
        "SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';",
        "START TRANSACTION;",
        "SET time_zone = '+00:00';"
    ]

    for tabletype in GameTable:
        query = ""
        query += f"CREATE TABLE `{tabletype.value}` ("

        table = tables[tabletype]
        if centralmanager.present[tabletype]:
            table = table.iloc[:,centralmanager.filter[tabletype]]
        print(table)
        for col in table.columns:
            query += f"`{table.loc[0, col]}` {table.loc[1,col]} NOT NULL, "
        query = query.removesuffix(", ")
        query += ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"

        queries += [query]


    queries += [
        f"ALTER TABLE `{GameTable.META.value}` ADD PRIMARY KEY (`gameid`);",
        f"ALTER TABLE `{GameTable.PLAYER.value}` ADD PRIMARY KEY (`gameid`,`participantid`);",
        f"ALTER TABLE `{GameTable.TEAM.value}` ADD PRIMARY KEY (`gameid`,`teamid`);",
        "COMMIT;"
    ]

    print(queries)
    return queries





def getCursorSelect(cur) -> pd.DataFrame:
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

    return pd.json_normalize(parsed_rows)
