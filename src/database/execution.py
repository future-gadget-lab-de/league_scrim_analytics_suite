import mariadb
import sys

def buildConnection(conn_params):
    """
    Uses connection parameters to build a connection and a cursor(interface with server) to a database host
    ----------
    Parameters
    ----------
        conn_params (dict):            Dicitonary containing connection data, read from /conf/database.conf
    ----------
    Return
    ----------
        conn    (connection):       Handles the connection to a MariaDB or MySQL database server. It encapsulates a database session.
        cur     (cursor):           Executes SQL statements and procedures, and manages fetching results.
    ----------
    """
    conn_params['port'] = int(conn_params['port']) 
    conn = mariadb.connect(**conn_params)
    cur = conn.cursor()
    return conn, cur

# Ich glaube hier muss eine Unterscheidung für Select und Insert queries gemacht werden.
def executeQuery(query, conn_params):
    conn, cur  = buildConnection(conn_params)

    try:
        cur.execute(query)
        conn.commit()
        cur.close()
        #TODO: Log query here.
    except mariadb.Error as e:
        cur.close()
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
