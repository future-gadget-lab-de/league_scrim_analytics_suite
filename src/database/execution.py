import mariadb
import sys

def buildConnection(conn_params: dict) -> tuple:
    """builds a connection to mariadb server

    Uses connection parameters to build a connection and a cursor(interface with server) to a database host

    Parameters
    ----------
    conn_params : dict
        Dicitonary containing connection data, read from /conf/database.conf

    Returns
    -------
    conn : connection
        Handles the connection to a MariaDB or MySQL database server. It encapsulates a database session. 
    cur : cursor
        Executes SQL statements and procedures, and manages fetching results.
    """
    conn_params['port'] = int(conn_params['port']) 
    conn = mariadb.connect(**conn_params)
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
            cur.execute(query)
            print("INFO: "+query + "\n")
            conn.commit()
            #TODO: Log query here.
        except mariadb.Error as e:
            cur.close()
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
    
